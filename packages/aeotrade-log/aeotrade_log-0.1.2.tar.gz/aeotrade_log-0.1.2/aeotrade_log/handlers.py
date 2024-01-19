import os
import time
from logging import Formatter
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path

import shutil
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

log_path = os.path.join(BASE_DIR, "logs")


class MyLogFormatter(Formatter):
    """rewrite Formatter class"""

    default_msec_format = "%s.%03d"


class MonthlyRotatingFileHandler(TimedRotatingFileHandler, RotatingFileHandler):
    """
    rewrite TimedRotatingFileHandler and RotatingFileHandler class, auto create folder, and places the scrolling
    number after the date
    """

    def __init__(
            self,
            filename,
            when="M",
            interval=60,
            backupCount=0,
            maxBytes=0,
            encoding=None,
            delay=False,
            utc=False,
            atTime=None,
            *args,
            **kwargs
    ):
        folder = os.path.dirname(filename)
        if not os.path.exists(folder):
            os.makedirs(folder)
        super().__init__(
            filename, when, interval, backupCount, encoding, delay, utc, atTime
        )
        RotatingFileHandler.__init__(
            self,
            filename,
            mode="a",
            maxBytes=maxBytes,
            backupCount=backupCount,
            encoding=encoding,
            delay=delay,
        )
        self.rolloverAt = self.init_rolloverAt()
        self.os = os.name
        self.base_dir = kwargs.get("BASE_DIR", BASE_DIR)
        self.log_path = os.path.join(self.base_dir, "logs")

    def init_rolloverAt(self):

        now = datetime.now()
        next_hour = now + (timedelta(hours=1) - timedelta(minutes=now.minute, seconds=now.second,
                                                          microseconds=now.microsecond))

        timestamp = int(time.mktime(next_hour.timetuple()))
        return timestamp

    def doDelete(self):
        """
        Delete old log folders
        """

        backup_cutoff_date = datetime.now() - timedelta(
            days=self.backupCount
        )  # Subtract backupCount * 60 days
        for backup_month_dir in os.listdir(self.log_path):
            month_dir = os.path.join(self.log_path, backup_month_dir)

            if not os.path.isdir(month_dir):
                continue

            for backup_date_dir in os.listdir(month_dir):
                try:
                    backup_date = datetime.strptime(backup_date_dir, "%Y-%m-%d")
                except Exception as e:
                    continue
                if backup_date < backup_cutoff_date:
                    shutil.rmtree(os.path.join(month_dir, backup_date_dir))

            # 判断backup_date_dir是否为空文件夹，如果是则删除
            if not os.listdir(month_dir):
                shutil.rmtree(month_dir)

    def split_last(self, result):
        driver = ""
        separator = "/"
        if self.os == "nt":
            sp = result.split(":")
            driver, result = sp[0] + ":", sp[1]
            separator = "\\"
        s_reverse = result[::-1]
        pos = s_reverse.find(separator)
        folder_reverse, file_name_reverse = s_reverse[pos + 1:], s_reverse[:pos]
        return driver + folder_reverse[::-1], file_name_reverse[::-1]

    def rotation_filename(self, default_name: str) -> str:
        result = super().rotation_filename(default_name)

        suffix = datetime.now().strftime(self.suffix)
        result_list = result.split(".")
        result_list[-1] = suffix
        new_result = ".".join(result_list)
        folder, file_name = self.split_last(new_result)
        full_folder = "%s/%s/%s" % (
            folder,
            time.strftime("%Y-%m"),
            time.strftime("%Y-%m-%d"),
        )
        if not os.path.exists(full_folder):
            os.makedirs(full_folder)
        new_file_name = (
                file_name.split(".")[0]
                + "-"
                + time.strftime("%Y-%m-%d-%H")
                + ".log"
                + "."
                + file_name.split(".")[-1]
        )
        return full_folder + "/%s" % new_file_name

    def doRollover(self):
        """
        Override doRollover method to implement custom log rotation and archiving
        """
        super().doRollover()
        if self.backupCount > 0:
            self.doDelete()

        self.rolloverAt = self.init_rolloverAt()  # 重新计算rollover

    def shouldRollover(self, record):
        """
        Determine if rollover should occur.
        """
        if super().shouldRollover(
                record
        ):  # Check if TimedRotatingFileHandler requires rollover based on time
            return True
        if (
                self.stream is None
        ):  # Check if RotatingFileHandler requires rollover based on file size
            self.stream = self._open()
        return self.stream.tell() >= int(self.maxBytes)
