import os
import time
import sys

class Reloader:
    def __init__(self, file_path = sys.argv[0], args = None, reload_time=None):
        """
        :param file_path: (str) Absolute path of file ex: /Users/abc/main.py
        :param args: List[str] extra args required for program ex: /Users/abc/main.py --test -> args: --test
        :param reload_time: (int) Optional, expected amount of time after which reloader is expected to check for updates
        """
        self.file_path = file_path
        self.args = args
        self.reload_time = reload_time if reload_time else 5
        self.initial_last_modified_time = self.last_modified_checker()

    def last_modified_checker(self):
        """
            funtion to fetch last modified of the given file
        """
        return os.path.getmtime(self.file_path)

    def reloader(self):
        while True:
            if self.last_modified_checker() > self.initial_last_modified_time:
                args = [sys.executable, self.file_path]
                if self.args:
                     args += self.args
                os.execve(sys.executable, args, os.environ.copy())
            time.sleep(self.reload_time)
