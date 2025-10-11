#MIT License

#Copyright (c) 2025 kenftr

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.



import os
import inspect
from pathlib import Path

import yaml


def _get_caller_path(self):
    frame = inspect.stack()[1]
    caller_path = Path(frame.filename).resolve()
    return caller_path
#default variable

class config():
    @staticmethod
    def make() -> Path:
        """
        EN:
            Create and return the path of the config path. If it already exists, it will not be created..
        VI:
            Tạo và trả về path của config. Nếu đã có thì không tạo nữa mà chỉ trả về

        :returns:
            Path: ~/.plugins/<plugin_name>/config.yml
        """
        try:
            caller_path = _get_caller_path()

            plugin_name = caller_path.parent.name

            config_path = (Path(__file__).parent.parent.parent / "plugins" / plugin_name / "config.yml")

            config_path.parent.mkdir(parents=True, exist_ok=True)

            if not config_path.exists():
                config_path.touch()

            return config_path
        except Exception as e:
            raise e
    @staticmethod
    def read(config_name = 'config.yml') -> dict:
        """
        EN:
            Read the specified config file. If not specified, defaults to reading "config.yml".

        VI:
            Đọc file config chỉ định. Nếu không chỉ định, mặc định sẽ đọc "config.yml".

        Args:
            config_name (str, optional): Config file name. Default is "config.yml".

        Returns:
            dict: The YAML data loaded into a Python dictionary.

        Raises:
            FileNotFoundError: If the config file does not exist. To create it, use `Config.make()`.
            RuntimeError: If an error occurs while loading the YAML.
        """
        caller_path = _get_caller_path()

        plugin_name = caller_path.parent.name

        config_path = (Path(__file__).parent.parent.parent / ".plugins" / plugin_name / "config.yml" if config_name == "config-yml" else config_name)

        if not config_path.exists():
            raise FileNotFoundError("config not found")
        try:
            with open(config_path,'r',encoding='utf-8') as f:
                return yaml.load(f,Loader=yaml.SafeLoader)
        except Exception as e:
            raise RuntimeError(f"Error loading YAML config: {e}")
