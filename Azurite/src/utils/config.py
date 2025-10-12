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
import yaml
from functools import lru_cache


def _to_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ("enable", "true", "yes", "1")
    return False


@lru_cache(maxsize=1)
def _load_yaml() -> dict:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..'))
    config_path = os.path.join(base_dir, 'azurite.yml')

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


class Config:

    data = _load_yaml()

    class Discord:
        @staticmethod
        def bot_token() -> str:
            return Config.data.get('discord', {}).get('bot_token', '')

        @staticmethod
        def intents() -> list:
            return Config.data.get('discord', {}).get('intents', [])

        @staticmethod
        def auto_sharded() -> bool:
            return _to_bool(Config.data.get('discord', {}).get('auto_sharded', False))

        @staticmethod
        def command_prefix() -> str:
            return Config.data.get('discord', {}).get('command_prefix', '!')

        @staticmethod
        def sync() -> str:
            return Config.data.get('discord', {}).get('sync', 'all_guilds')
    class Loader:
        @staticmethod
        def multi_thread() -> bool:
            return _to_bool(Config.data.get('Loader', {}).get('multi_thread', False))

        @staticmethod
        def max_thread() -> int:
            return Config.data.get('Loader', {}).get('max_thread', -1)
        @staticmethod
        def fast_module() -> bool:
            return _to_bool(Config.data.get('Loader', {}).get('fast_module', False))
        @staticmethod
        def timed_out() -> int:
            return Config.data.get('Loader', {}).get('timed_out', 5000)

        class Allow:
            @staticmethod
            def prefix_command() -> bool:
                return _to_bool(Config.data.get('Loader', {}).get('allow', {}).get('prefix_command', '!'))

            @staticmethod
            def slash_command() -> bool:
                return _to_bool(Config.data.get('Loader', {}).get('allow', {}).get('slash_command', False))

            @staticmethod
            def group_command() -> bool:
                return _to_bool(Config.data.get('Loader', {}).get('allow', {}).get('group_command', False))

            @staticmethod
            def events() -> bool:
                return _to_bool(Config.data.get('Loader', {}).get('allow', {}).get('events', False))

            @staticmethod
            def plugin_format() -> list:
                return Config.data.get('Loader', {}).get('allow', {}).get('plugin_format', [])

        class ScriptLoader:
            @staticmethod
            def status() -> bool:
                return _to_bool(Config.data.get('Loader', {}).get('script_loader', {}).get('enable', False))
            @staticmethod
            def disable_script_list() -> list:
                return Config.data.get('Loader',{}).get('script_loader',{}).get('disable_script_list', [])
    class Azurite:
        class Package:
            @staticmethod
            def embed_format() -> str:
                return Config.data.get('Azurite', {}).get('package', {}).get('embed_format', 'default')


    @staticmethod
    def Mapping() -> dict:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
        mapping_config_path = os.path.join(base_dir, 'config','mapping.yml')
        if not os.path.exists(mapping_config_path):
            return None
        with open(mapping_config_path,'r',encoding='utf-8') as f:
            data = yaml.load(f,yaml.SafeLoader)
        return data