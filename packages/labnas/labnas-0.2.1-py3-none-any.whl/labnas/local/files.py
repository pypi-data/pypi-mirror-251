import socket
from pathlib import Path


def get_path_to_base() -> Path:
    host_name = socket.gethostname()
    if host_name == "mathis-Precision-Tower-3431":
        path = Path("/home/mathis/Code/gitlab/labnas")
    elif host_name == "matt-bluechip-BUSINESSline-individu":
        path = Path("/home/matt/Code/labnas")
    elif host_name == "DESKTOP-RI6NU4C":
        path = Path("C:/Users/widefield/Mathis/gitlab/labnas")
    else:
        raise ValueError(f"{host_name=} unknown")
    return path
