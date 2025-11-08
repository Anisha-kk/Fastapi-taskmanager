import logging.config
from datetime import datetime
from pathlib import Path

import pytz


class IndianTimeFormatter(logging.Formatter):
    def converter(self, timestamp):
        dt = datetime.fromtimestamp(timestamp)
        dt = dt.replace(tzinfo=pytz.utc)
        return dt.astimezone(pytz.timezone('Asia/Kolkata'))

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            s = dt.strftime(datefmt)  # [:-3]
        else:
            try:
                s = dt.isoformat(timespec='milliseconds')
            except TypeError:
                s = dt.isoformat()
        return s


class Logger:
    LOG_DIR = f"logs"
    Path(LOG_DIR).mkdir(mode=0o777, parents=True, exist_ok=True)

    @staticmethod
    def logger(logger_name):
        config_file = Path(Path(__file__).parent,
                           "logger.conf").resolve(strict=True)
        logging.config.fileConfig(
            fname=config_file, disable_existing_loggers=False, defaults={'logdirpath': Logger.LOG_DIR})
        logger = logging.getLogger(logger_name)
        return logger
