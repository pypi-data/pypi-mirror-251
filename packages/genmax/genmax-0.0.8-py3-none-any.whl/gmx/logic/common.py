import os
import subprocess
import platform

class CommonLogic:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def get_gmx_folder_path(folder_path):
        if platform.system() != "Windows":
            folder_path = "_" + folder_path
        return folder_path
