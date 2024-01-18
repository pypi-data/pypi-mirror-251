"""NAS interactions specific to imaging data."""
import os
import re
import time
from pathlib import Path

import numpy as np
import tifffile
import zarr
from tqdm import tqdm
from tifffile.tifffile import TiffFileError

from labnas.remote.base import SftpNas
from labnas.local.base import identify_tif_origin, TifFileMissingException
from labnas.local.base import assert_single_stack, sort_tif_files


class ImagingNas(SftpNas):
    """Extends SftpNas for imaging data."""

    def sort_folder(
            self,
            remote_folder: Path,
            local_temp_folder: Path,
            remote_trash_folder: Path,
            recursive: bool = True,
            level: int = 0,
    ) -> None:
        """Sort a folder with imaging .tif files."""
        self.logger.info(f"=> Investigating: {remote_folder} (Level: {level})")
        if "INCOMPLETE" in remote_folder.name:
            self.logger.info(f"Skipping {remote_folder} -> INCOMPLETE flag.")
        elif "multipage" in remote_folder.name:
            self.logger.info(f"Skipping {remote_folder} -> multipage flag.")
        else:
            stacks, single_tifs = self.check_folder_structure(remote_folder)
            for stack_name, stack_tifs in stacks.items():
                self.process_stack(
                    stack_name=stack_name,
                    stack_tifs=stack_tifs,
                    remote_folder=remote_folder,
                    local_temp_folder=local_temp_folder,
                    remote_trash_folder=remote_trash_folder,
                )
            if recursive:
                _, folders = self.list_files_and_folders(remote_folder)
                for folder in folders:
                    self.sort_folder(folder, local_temp_folder, remote_trash_folder, level=level + 1)

    def process_stack(self, stack_name: str, stack_tifs: list, remote_folder: Path, local_temp_folder: Path, remote_trash_folder: Path) -> None:
        """
        1. Download stack as multipage tif.
        2. Upload multipage tif.
        3. Delete local multipage tif.
        4. Delete nas stack tifs.
        """
        # set paths
        remote_tif = remote_folder / "multipage_tiff" / f"{stack_name}.tif"
        self.logger.info(f"---{remote_tif}---")
        if self.is_file(remote_tif):
            raise FileExistsError(f"{remote_tif}")
        if not self.is_dir(remote_tif.parent):
            self.create_empty_folder(remote_tif.parent)
            self.logger.info(f"{remote_tif.parent} created.")
        self.logger.info(f"Downloading {stack_name} as as single tif.")

        trash_name = remote_folder / stack_name
        trash_name = str(trash_name).replace("/", "_")
        stack_trash_folder = remote_trash_folder / trash_name
        if self.is_file(stack_trash_folder):
            raise FileExistsError(f"{stack_trash_folder}")

        try:
            # 1. Download stack as multipage tif
            local_tif = self.download_files_as_single_tif(
                tif_files=stack_tifs,
                file_name=f"{stack_name}.tif",
                local_folder=local_temp_folder,
            )

            # 2. Upload multipage tif
            self.logger.info(f"Uploading {local_tif}")
            self.upload_file(local_tif, remote_tif)
            self.logger.info(f"Uploaded {local_tif} as {remote_tif}")

            # 3. Delete local multipage tif
            self.safely_delete(local_tif)

            # 4. Move stack tifs to trash
            self.create_empty_folder(stack_trash_folder)
            self.logger.info(f"Moving stack tifs to {stack_trash_folder}")
            for file in tqdm(stack_tifs):
                trash_path = stack_trash_folder / file.name
                self.move_file(file, trash_path)
        except (TifFileMissingException, TiffFileError) as e:
            self.logger.error(f"{e}")
            self.logger.info("Moving tifs into separate folder instead of combining.")
            incomplete_target = remote_folder / f"INCOMPLETE_{stack_name}"
            self.create_empty_folder(incomplete_target)
            self.logger.info(f"Moving stack tifs to {incomplete_target}")
            for file in tqdm(stack_tifs):
                new_path = incomplete_target / file.name
                self.move_file(file, new_path)

    def safely_delete(self, local_tif: Path, n_attempts: int = 3) -> bool:
        count = 0
        successful = False
        while count < n_attempts:
            try:
                os.remove(local_tif)
                self.logger.info(f"Removed {local_tif}")
                successful = True
                break
            except PermissionError as pe:
                self.logger.info(f"Could not remove {local_tif} on attempt {count + 1}: {pe}")
                time.sleep(10)
                count += 1
        if not successful:
            self.logger.warning(f"Failed to remove {local_tif} after {count} attempts.")
        return successful

    def check_folder_structure(self, remote_folder: Path) -> tuple[dict, list]:
        """
        Check if a folder contains .tif files belonging to more than 1 stack.
        Also return stacks and tifs because scanning large folders takes time.
        """
        tifs = self.find_tifs_in_folder(remote_folder)
        if len(tifs) == 0:
            self.logger.info(f"No tifs in {remote_folder}.")
            stacks = {}
            single_tifs = []
        elif len(tifs) == 1:
            self.logger.info(f"Only 1 tif: {tifs[0]}.")
            stacks = {}
            single_tifs = tifs
        else:
            self.logger.info(f"{len(tifs)} tifs in {remote_folder} - looking for stacks.")
            stacks, single_tifs = self.identify_stacks_in_tifs(tifs)
        return stacks, single_tifs

    def find_tifs_in_folder(self, remote_folder: Path) -> list[Path]:
        """Find tif files in a nas folder."""
        files, folders = self.list_files_and_folders(remote_folder)
        tifs = self.identify_tifs_in_files(files)
        return tifs

    @staticmethod
    def identify_tifs_in_files(files: list[Path]) -> list[Path]:
        """Identify tif files in a list of files."""
        tifs = []
        for file in files:
            if file.suffix in [".tif", ".tiff"]:
                tifs.append(file)
        return tifs

    def identify_stacks_in_tifs(self, tifs: list[Path]) -> tuple[dict, list]:
        """Identify if tifs come from multi-frame recordings or if they are single snapshots.."""
        tif_origin = identify_tif_origin(tifs[0])
        if tif_origin == "leica":
            self.logger.info(f"Tifs (e.g. {tifs[0].name}) identified as leica tifs")
            stacks, single_tifs = self.identify_leica_stacks_in_tifs(tifs)
        elif tif_origin == "basler":
            self.logger.info(f"Tifs (e.g. {tifs[0].name}) identified as basler tifs")
            stacks, single_tifs = self.identify_basler_stacks_in_tifs(tifs)
        elif tif_origin == "leica_metadata":
            self.logger.info(f"{tifs[0].parent} identified as leica metadata tifs.")
            single_tifs = tifs
            stacks = {}
        else:
            self.logger.info(f"Could not identify stacks: neither leica nor basler.")
            single_tifs = tifs
            stacks = {}
        self.logger.info(f"{len(stacks)} tif stacks and {len(single_tifs)} single tifs found.")
        return stacks, single_tifs

    def identify_leica_stacks_in_tifs(self, tifs: list[Path]) -> tuple[dict, list]:
        """Sort tif files into stacks belonging to a single recording."""
        stacks = {}
        single_tifs = []
        for file in tifs:
            file_name = file.name
            findings = re.findall("_[zt][0-9]+_", file_name)
            if findings:
                splitter = findings[0]
                parts = file_name.split(splitter)
                stack_name = parts[0]
                if stack_name not in stacks.keys():
                    self.logger.info(f"Stack in {tifs[0].parent}: {stack_name}")
                    stacks[stack_name] = []
                stacks[stack_name].append(file)
            else:
                single_tifs.append(file)
        keys_to_delete = []
        for stack_name, stack_list in stacks.items():
            if len(stack_list) == 1:
                single_tifs.append(stack_list[0])
                keys_to_delete.append(stack_name)
                self.logger.info(f"Only 1 tif in stack {stack_name} -> Appending to single tifs.")
        for key in keys_to_delete:
            del stacks[key]
        return stacks, single_tifs

    @staticmethod
    def identify_basler_stacks_in_tifs(tifs: list[Path]) -> tuple[dict, list]:
        """Sort tif files into stacks belonging to a single recording."""
        stacks = {}
        single_tifs = []
        for file in tifs:
            parts = file.name.split("_")
            index_part = parts[-1]
            stack_name = "_".join(parts[:-1])
            if stack_name not in stacks.keys():
                stacks[stack_name] = []
            stacks[stack_name].append(file)
        return stacks, single_tifs

    def create_folder_for_stack(self, stack_name: str, remote_folder: Path, stack_files: list[Path]) -> None:
        """Move .tif files belonging to a single stack into a dedicated folder."""
        self.logger.info(f"{len(stack_files)} tifs in stack {stack_name}.")
        parent_directory = remote_folder / stack_name
        if parent_directory.is_dir():
            raise FileExistsError(f"{parent_directory}")
        self.connection.mkdir(str(parent_directory))
        for file in tqdm(stack_files):
            new_path = parent_directory / file.name
            self.move_file(file, new_path)
        self.logger.info(f"Moved {len(stack_files)} tifs into {parent_directory}.")

    def download_files_as_single_tif(self, tif_files: list, file_name: str, local_folder: Path) -> Path:
        temp_local = local_folder / "temp.tif"
        multipage_local = local_folder / file_name
        assert multipage_local.suffix == ".tif"

        n_files = len(tif_files)
        self.logger.info(f"{len(tif_files)} tif files")
        assert n_files > 1, f"Not enough files: {n_files=} < 1"
        assert_single_stack(tif_files)
        tif_files = sort_tif_files(tif_files)
        for i_file in tqdm(range(n_files)):
            file = tif_files[i_file]
            self.download_file(file, temp_local, overwrite=True)
            image = tifffile.imread(temp_local)
            if i_file == 0:
                shape = (n_files, image.shape[0], image.shape[1])
                tifffile.imwrite(
                    multipage_local,
                    shape=shape,
                    dtype=np.uint8,
                )
                store = tifffile.imread(multipage_local, mode="r+", aszarr=True)
                z = zarr.open(store, mode="r+")
                self.logger.info(f"Empty tif created: {shape}")
            z[i_file, :, :] = image
        os.remove(local_folder / "temp.tif")
        return multipage_local

    def download_folder_as_single_tif(self, remote_folder: Path, local_folder: Path) -> Path:
        """Download each tif of a stack, save into a singe local tif."""
        temp_local = local_folder / "temp.tif"
        multipage_local = local_folder / f"{remote_folder.name}.tif"
        tif_files = self.find_tifs_in_folder(remote_folder)
        n_files = len(tif_files)
        self.logger.info(f"{len(tif_files)} tif files in {remote_folder}")
        assert n_files > 1, f"Not enough files in {remote_folder}: {n_files} < 1"
        assert_single_stack(tif_files)
        tif_files = sort_tif_files(tif_files)
        for i_file in tqdm(range(n_files)):
            file = tif_files[i_file]
            self.download_file(file, temp_local, overwrite=True)
            image = tifffile.imread(temp_local)
            if i_file == 0:
                shape = (n_files, image.shape[0], image.shape[1])
                tifffile.imwrite(
                    multipage_local,
                    shape=shape,
                    dtype=np.uint8,
                )
                store = tifffile.imread(multipage_local, mode="r+", aszarr=True)
                z = zarr.open(store, mode="r+")
                self.logger.info(f"Empty tif created: {shape}")
            z[i_file, :, :] = image
        os.remove(local_folder / "temp.tif")
        return multipage_local
