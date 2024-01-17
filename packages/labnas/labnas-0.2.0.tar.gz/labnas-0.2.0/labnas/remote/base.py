"""Basic connection to a network-associated server (NAS)."""
import logging
import os
import sys
from pathlib import Path, PurePath, PurePosixPath

import pysftp
from tqdm import tqdm


PathLike = Path | PurePath


class SftpNas:
    """Basic SFTP connection (wrapper around pysftp)"""

    def __init__(self, host_name: str, user_name: str, pwd: str, log_file: Path | None = None) -> None:
        """Create pysftp.Connection to server."""
        self._host_name = host_name
        self._user_name = user_name
        self._pwd = pwd
        self.log_file = log_file
        self.logger = self.create_logger()
        self.connection: pysftp.Connection = pysftp.Connection(
            host=host_name,
            username=user_name,
            password=pwd,
        )
        self.logger.info(f"Connection established: {host_name}@{user_name}")

    def create_logger(self) -> logging.Logger:
        logger = logging.Logger("nas")
        logger.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        if isinstance(self.log_file, Path):
            file_handler = logging.FileHandler(self.log_file)
            formatter = logging.Formatter("%(asctime)s - %(message)s")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            logger.info(f"Logging into {self.log_file}")
        return logger

    def close(self) -> None:
        """Close connection."""
        self.connection.close()

    def reconnect(self) -> None:
        try:
            self.connection.close()
        except Exception as e:
            self.logger.info(f"Could not close connection: {e}")
        self.connection: pysftp.Connection = pysftp.Connection(
            host=self._host_name,
            username=self._user_name,
            password=self._pwd,
        )

    def list_contents(self, remote_folder: PathLike) -> list[PathLike]:
        """List contents of a nas folder"""
        remote_folder = self._convert_to_linux(remote_folder)
        if not self.is_dir(remote_folder):
            raise FileNotFoundError(f"{remote_folder} not found.")
        contents: list[str] = self.connection.listdir(str(remote_folder))
        contents: list[PathLike] = [remote_folder / name for name in contents]
        return contents

    def is_dir(self, remote_path: PathLike) -> bool:
        """Check whether a nas path is a directory."""
        remote_path = self._convert_to_linux(remote_path)
        return self.connection.isdir(str(remote_path))

    def list_files_and_folders(self, remote_folder: PathLike) -> tuple:
        """List contents of a nas folder sorted into files and folders"""
        files = []
        folders = []
        remote_folder = self._convert_to_linux(remote_folder)
        contents = self.list_contents(remote_folder)
        for element in contents:
            if self.is_file(element):
                files.append(element)
            elif self.is_dir(element):
                folders.append(element)
            else:
                raise ValueError(f"{element} is neither file nor folder?")
        return files, folders

    def is_file(self, remote_path: PathLike) -> bool:
        """Check whether a nas path is a file."""
        remote_path = self._convert_to_linux(remote_path)
        return self.connection.isfile(str(remote_path))

    def download_file(self, remote_file: Path, local_file: Path, overwrite: bool = False) -> None:
        """Download a single file from the server"""
        remote_file = self._convert_to_linux(remote_file)
        if not self.is_file(remote_file):
            raise FileNotFoundError(f"{remote_file} does not exist.")
        if not local_file.parent.is_dir():
            raise FileNotFoundError(f"Target parent folder {local_file.parent} does not exist.")
        if local_file.is_file() and not overwrite:
            raise FileExistsError(f"{local_file} already exists.")
        self.connection.get(str(remote_file), str(local_file))

    def upload_file(self, local_file: Path, remote_file: Path) -> None:
        """Upload a single file to the server"""
        remote_file = self._convert_to_linux(remote_file)
        if not local_file.is_file():
            raise FileNotFoundError(f"{local_file} does not exist.")
        if not self.is_dir(remote_file.parent):
            raise FileNotFoundError(f"Target parent folder {remote_file.parent} does not exist.")
        if self.is_file(remote_file):
            raise FileExistsError(f"{remote_file} already exists.")
        self.connection.put(str(local_file), str(remote_file))

    def download_folder(self, remote_folder: Path, local_parent: Path, recursive: bool = True) -> Path:
        """Download a whole folder from the server"""
        remote_folder = self._convert_to_linux(remote_folder)
        if not self.is_dir(remote_folder):
            raise FileNotFoundError(f"{remote_folder} does not exist.")
        if not local_parent.is_dir():
            raise FileNotFoundError(f"Target parent folder {local_parent} does not exist.")
        local_folder = local_parent / remote_folder.name
        if local_folder.is_dir():
            raise FileExistsError(f"{local_folder} already exists.")
        os.mkdir(local_folder)
        files, folders = self.list_files_and_folders(remote_folder)
        self.logger.info(f"{len(files)} files found in {remote_folder}.")
        self.logger.info(f"{len(folders)} folders found in {remote_folder}.")
        for remote_file in tqdm(files):
            local_file = local_folder / remote_file.name
            self.download_file(remote_file, local_file)
        if recursive:
            for remote_sub_folder in folders:
                self.download_folder(remote_sub_folder, local_folder, recursive=recursive)
        return local_folder

    def upload_folder(self, local_source: Path, remote_parent: PathLike, recursive: bool = True, make_tree: bool = False) -> PathLike:
        """Upload a folder to the NAS"""
        remote_parent = self._convert_to_linux(remote_parent)
        if not local_source.is_dir():
            raise FileNotFoundError(f"{local_source} does not exist.")
        if not self.is_dir(remote_parent):
            if make_tree:
                self.connection.makedirs(str(remote_parent))
                self.logger.info(f"Folder tree to {remote_parent} created.")
            else:
                raise FileNotFoundError(f"{remote_parent} does not exist.")

        # create nas folder
        remote_target = remote_parent / local_source.name
        if self.connection.isdir(str(remote_target)):
            raise FileExistsError(f"{remote_target} already exists.")
        self.connection.mkdir(str(remote_target))
        self.logger.info(f"Remote folder {remote_target} created.")

        # get contents of local folder
        files, folders = self.list_local_files_and_folders(local_source)

        # upload files
        for local_file in files:
            remote_file = remote_target / local_file.name
            self.upload_file(local_file, remote_file)
            self.logger.info(f"{local_file} -> {remote_file}")

        # upload sub-folders
        if recursive:
            for local_sub_folder in folders:
                self.upload_folder(local_sub_folder, remote_target)
        return remote_target

    def print_tree(self, remote_folder: Path, recursive: bool = True, level: int = 0, max_level: int = 3) -> None:
        """Print file tree."""
        remote_folder = self._convert_to_linux(remote_folder)
        if level < max_level:
            files, folders = self.list_files_and_folders(remote_folder)
            indent = f"\t" * level
            for file in files:
                self.logger.info(f"{indent} {file.name}")

            for folder in folders:
                self.logger.info(f"{indent} {folder.name}")
                if recursive:
                    self.print_tree(folder, level=level + 1, max_level=max_level)

    @staticmethod
    def list_local_files_and_folders(local_folder: Path) -> tuple:
        """List local files and folders."""
        elements = local_folder.iterdir()
        files = []
        folders = []
        for element in elements:
            if element.is_file():
                files.append(element)
            elif element.is_dir():
                folders.append(element)
            else:
                raise ValueError(f"{element} is neither file nor folder?")
        return files, folders

    def move_file(self, remote_source: Path, remote_target: Path) -> None:
        """Move a file around."""
        remote_source = self._convert_to_linux(remote_source)
        remote_target = self._convert_to_linux(remote_target)
        if not self.is_file(remote_source):
            raise FileNotFoundError(f"{remote_source}")
        if self.is_file(remote_target):
            raise FileExistsError(f"{remote_target}")
        if not self.is_dir(remote_target.parent):
            raise FileNotFoundError(f"{remote_target.parent}")
        self.connection.rename(str(remote_source), str(remote_target))

    def move_folder(self, remote_source: Path, remote_target: Path) -> None:
        """Move a folder from one nas location to another."""
        remote_source = self._convert_to_linux(remote_source)
        remote_target = self._convert_to_linux(remote_target)
        if not self.is_dir(remote_source):
            raise FileNotFoundError(f"{remote_source} does not exist.")
        if self.is_dir(remote_target):
            raise FileExistsError(f"{remote_target} already exists.")
        self.connection.rename(str(remote_source), str(remote_target))

    def create_empty_folder(self, remote_folder: Path) -> None:
        """Create empty folder on NAS."""
        remote_folder = self._convert_to_linux(remote_folder)
        if self.is_dir(remote_folder):
            raise FileExistsError(f"{remote_folder} already exists.")
        self.connection.makedirs(str(remote_folder))

    def get_file_size(self, remote_file: Path, unit: str = "gb") -> float:
        """Get size of a remote file."""
        remote_file = self._convert_to_linux(remote_file)
        stats = self.connection.stat(str(remote_file))
        file_size = stats.st_size
        if unit == "gb":
            file_size = file_size / 10 ** 9
        else:
            raise NotImplementedError(f"{unit=} not implemented")
        return file_size

    @staticmethod
    def _convert_to_linux(remote_path: Path) -> PurePosixPath:
        """
        Convert remote path to PurePosixPath.
        This is for Windows compatibility.
        """
        assert isinstance(remote_path, (Path, PurePath)), f"{remote_path} is not a Path but {type(remote_path)}"
        remote_path = PurePosixPath(remote_path)
        return remote_path



