import os.path
import random
from datetime import datetime
from Swit.src.handler.file.path_manager import path

class log:
    @staticmethod
    def write_bug(data):
        """
        VI:
            Ghi dữ liệu traceback lỗi vào một file log và trả về đường dẫn file.

        EN:
            Write traceback data into a log file and return the file path.

        Args:
            data (str): The traceback data to be written into the file.

        Returns:
            str: The path to the created log file.
        """
        name = f"bug-traceback-{datetime.now().strftime('%Y%m%d - %H%M%S')}-{random.randint(1,20)}"
        file_path = os.path.join(path.root(),'logs',name)
        with open(file_path,'w', encoding='utf-8') as f:
            f.write(data)
        return file_path