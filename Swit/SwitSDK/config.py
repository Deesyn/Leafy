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



import inspect
import zipfile, rarfile
from pathlib import Path
from typing import Optional
import yaml
from Swit.src.handler.file.extract import extract

base_dir = (Path(__file__).parent.parent.parent)

class config():
    @staticmethod
    def _write_config(plugin_name,config_data):
        config_path = (Path(__file__).parent.parent.parent / "plugins" / "Plugin configs" / plugin_name / "config.yml")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        if not config_path.exists():
            config_path.touch()
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(config_data)
        return config_path
    @staticmethod
    def make(config_data = None) -> Path:
        """
        EN:
        Create and return the path to the config file.
        If the config already exists, it won't be recreated.
        You can pass either:
            - A string containing the config content, or
            - A path to an existing config file inside your plugin assets folder
              (e.g. './assets/{your_file}.yml').

        VI:
        Tạo và trả về đường dẫn đến file config.
        Nếu file đã tồn tại, hàm sẽ không tạo lại.
        Có thể truyền vào:
            - Chuỗi chứa nội dung config, hoặc
            - Đường dẫn đến file config trong thư mục assets của plugin
              (ví dụ: '/assets/{tên_file}.yml').

        Returns:
            Path: The full path to the config file (e.g. ~/.plugins/<plugin_name>/config.yml)
        """
        frame = inspect.stack()[1]
        caller_path = Path(frame.filename).resolve()
        temp_path = str(caller_path).split('\\')
        try:
            temp_plugin_path = caller_path.parts
            for i, value in enumerate(temp_plugin_path):
                if value.lower() == 'plugins':
                    plugin_name = caller_path.parts[i + 1]
                    break
            plugin_path = (Path(__file__).parent.parent.parent / "plugins" / plugin_name)
            plugin_config_path = (Path(__file__).parent.parent.parent / "plugins" / "Plugin configs" / plugin_name / "config.yml")

            if config_data is None:
                plugin_config_path.parent.mkdir(parents=True, exist_ok=True)

                if not plugin_config_path.exists():
                    plugin_config_path.touch()

                return plugin_config_path
            else:

                for i, name in enumerate(temp_path):
                    if name == 'plugins':
                        plugin_name = temp_path[i + 1]
                if plugin_path.is_dir():
                    with open((Path(__file__).parent.parent.parent / 'plugins' / plugin_name / config_data), 'r', encoding='utf-8') as f:
                        config_data = f.read()
                    config_path = config._write_config(plugin_name=plugin_name, config_data=config_data)
                    return config_path

                elif str((Path(__file__).parent.parent.parent / "plugins" / plugin_name)).endswith('zip') or str((Path(__file__).parent.parent.parent / "plugins" / plugin_name)).endswith('rar') and Path(config_data).suffix in (".yml", ".yaml", ".txt"):
                    if str(plugin_path).endswith('.zip'):
                        archive: Optional[zipfile.ZipFile] = extract.zip((Path(__file__).parent.parent.parent / 'plugins' / plugin_name))
                    if str(plugin_path).endswith('.rar'):
                        archive: Optional[rarfile.RarFile] = extract.rar((Path(__file__).parent.parent.parent / 'plugins' / plugin_name))
                    with archive.open(config_data) as f:
                        config_data = (f.read().decode('utf-8'))
                    config_path = config._write_config(plugin_name=plugin_name, config_data=config_data)
                    archive.close()
                    return config_path
                else:

                    config_path = config._write_config(plugin_name=plugin_name,config_data=config_data)
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
        frame = inspect.stack()[1]
        caller_path = Path(frame.filename).resolve()

        plugin_name = caller_path.parent.name

        config_path = (Path(__file__).parent.parent.parent / "plugins" / plugin_name / "Plugin configs" / "config.yml" if config_name == "config-yml" else config_name)

        if not config_path.exists():
            raise FileNotFoundError("config not found")
        try:
            with open(config_path,'r',encoding='utf-8') as f:
                return yaml.load(f,Loader=yaml.SafeLoader)
        except Exception as e:
            raise RuntimeError(f"Error loading YAML config: {e}")
