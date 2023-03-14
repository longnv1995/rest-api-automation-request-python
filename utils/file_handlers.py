import json
import yaml
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from pathlib import Path

from constants import SUPPORTED_FILE_EXTS, CONFIGS_DIR


def load_env_file():
    get_env_data = load_dotenv()
    return get_env_data

def get_absolute_path_to_file(file_name: str, folder_name: str=CONFIGS_DIR):
        root_dir = Path.cwd()
        absolute_path = Path.joinpath(root_dir, folder_name, file_name)
        return absolute_path

class BaseFormat(ABC):
    @abstractmethod
    def _read_file(self, file_name: str):
        pass

class JsonFormat(BaseFormat):
    def _read_file(self, file_name: str):
        absolute_path = get_absolute_path_to_file(file_name)

        with open(absolute_path, mode='r') as f:
            return json.load(f)
    
class IniFormat(BaseFormat):
    def _read_file(self, file_name: str):
        absolute_path = get_absolute_path_to_file(file_name)

        with open(absolute_path, mode='r') as f:
            pass

class YamlFormat(BaseFormat):
    def _read_file(self, file_name: str):
        absolute_path = get_absolute_path_to_file(file_name)

        with open(absolute_path, mode='r') as f:
            return yaml.safe_load(f)

class Configs:
    @staticmethod
    def load_file(file_name: str):
        ext = file_name.split('.')[1]

        if ext == SUPPORTED_FILE_EXTS[0]: # json format
            json_obj = JsonFormat()
            return json_obj._read_file(file_name)

        elif ext == SUPPORTED_FILE_EXTS[1]: # ini format
            init_obj = IniFormat()
            return init_obj._read_file(file_name)

        elif ext == SUPPORTED_FILE_EXTS[2]: # yaml format
            yaml_obj = YamlFormat()
            return yaml_obj._read_file(file_name)
        
        else:
            raise TypeError(f"Invalid file format. Only supported formats: {SUPPORTED_FILE_EXTS}")