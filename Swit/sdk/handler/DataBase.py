import os
import json
import inspect
import traceback
from pathlib import Path
import hashlib
from functools import lru_cache
from Swit.src.utils.Logger import Logger
from Swit.src.handler.file.log import log
from Swit.src.handler.file.path_manager import path


class DataBase:
    """
       A lightweight JSON-based database handler for Swit plugins.
       Automatically detects the plugin name based on the caller's path.
    """

    @staticmethod
    def create(reset_on_load: bool = False):
        """
        Create a new JSON database file for the plugin if it does not exist.

        Args:
            reset_on_load (bool): If True, overwrite existing file with an empty JSON object.

        Returns:
            dict: The loaded JSON data after creation or reset.
        """

        frame = inspect.stack()[1]
        caller_path = Path(frame.filename).resolve()
        temp_path = str(caller_path).split('\\')
        try:
            for i, value in enumerate(temp_path):
                print(i, value)
                if value.lower() == 'plugins':
                    plugin_name = caller_path.parts[i + 1]
                    break
        except Exception as e:
            Logger.ERROR("Cannot find the plugins folder")
            traceback_file = log.write_bug(traceback.format_exc())
            Logger.ERROR(f"The bug details are saved at {traceback_file}")


        database_path = os.path.join(path.root(), 'data', 'database', f"{plugin_name}.json")

        if not os.path.exists(database_path):
            with open(database_path, 'w', encoding='utf-8') as f:
                f.write('{}')

        if reset_on_load:
            with open(database_path, 'w', encoding='utf-8') as f:
                f.write('{}')
            with open(database_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            with open(database_path, 'r', encoding='utf-8') as f:
                return json.load(f)

    @staticmethod
    def read():
        """
        Read and return the contents of the plugin's database file.

        Returns:
            dict: Parsed JSON data from the database file.
                  Returns an error dictionary if the file does not exist.
        """

        frame = inspect.stack()[1]
        caller_path = Path(frame.filename).resolve()
        temp_path = str(caller_path).split('\\')
        try:
            for i, value in enumerate(temp_path):
                print(i, value)
                if value.lower() == 'plugins':
                    plugin_name = caller_path.parts[i + 1]
                    break
        except Exception as e:
            Logger.ERROR("Cannot find the plugins folder")
            traceback_file = log.write_bug(traceback.format_exc())
            Logger.ERROR(f"The bug details are saved at {traceback_file}")

        database_path = os.path.join(path.root(), 'data', 'database', f"{plugin_name}.json")

        if not os.path.exists(database_path):
            return {
                "status_code": 0,
                "details": "Database file not found, please call create() before reading"
            }

        with open(database_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def write(data: dict):
        """
        Overwrite the plugin's database file with new data.

        Args:
            data (dict): The new data to write to the database.

        Returns:
            list: [new_data, old_data] after writing.
                  Returns an error dictionary if the file does not exist.
        """

        frame = inspect.stack()[1]
        caller_path = Path(frame.filename).resolve()
        temp_path = str(caller_path).split('\\')
        try:
            for i, value in enumerate(temp_path):
                print(i, value)
                if value.lower() == 'plugins':
                    plugin_name = caller_path.parts[i + 1]
                    break
        except Exception as e:
            Logger.ERROR("Cannot find the plugins folder")
            traceback_file = log.write_bug(traceback.format_exc())
            Logger.ERROR(f"The bug details are saved at {traceback_file}")

        database_path = os.path.join(path.root(), 'data', 'database', f"{plugin_name}.json")

        if not os.path.exists(database_path):
            return {
                "status_code": 0,
                "details": "Database file not found, please call create() before writing"
            }

        with open(database_path, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)

        with open(database_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return [data, backup_data]

    @staticmethod
    def remove():
        """
        Remove the plugin's database file from disk.

        Returns:
            dict: A result dictionary indicating success or failure.
        """

        frame = inspect.stack()[1]
        caller_path = Path(frame.filename).resolve()
        temp_path = str(caller_path).split('\\')
        try:
            for i, value in enumerate(temp_path):
                print(i, value)
                if value.lower() == 'plugins':
                    plugin_name = caller_path.parts[i + 1]
                    break
        except Exception as e:
            Logger.ERROR("Cannot find the plugins folder")
            traceback_file = log.write_bug(traceback.format_exc())
            Logger.ERROR(f"The bug details are saved at {traceback_file}")

        database_path = os.path.join(path.root(), 'data', 'database', f"{plugin_name}.json")

        if not os.path.exists(database_path):
            return {
                "status_code": 0,
                "details": "Database file not found"
            }

        try:
            os.remove(database_path)
            return {
                "status_code": 1,
                "details": "Database file removed successfully"
            }
        except Exception as e:
            traceback_file = log.write_bug(traceback.format_exc())
            Logger.ERROR(f"Failed to remove database file: {e}")
            return {
                "status_code": -1,
                "details": f"Error occurred, see {traceback_file}"
            }