import logging.handlers


class LogWriter:
    log = logging.getLogger("LogWriter")
    formatter = logging.Formatter('[%(asctime)s][%(levelname)-8s] %(message)s : (%(filename)s:%(lineno)s)',
                                  datefmt='%H:%M:%S')
    fileHandler = None

    @staticmethod
    def set_log_level(level):
        if level == "INFO":
            LogWriter.log.setLevel(logging.INFO)
        elif level == "WARNING":
            LogWriter.log.setLevel(logging.WARNING)
        elif level == "ERROR":
            LogWriter.log.setLevel(logging.ERROR)
        elif level == "CRITICAL":
            LogWriter.log.setLevel(logging.CRITICAL)
        else:
            LogWriter.log.setLevel(logging.DEBUG)

    @staticmethod
    def set_log_file(log_file):
        LogWriter.fileHandler = logging.handlers.TimedRotatingFileHandler(log_file, when='midnight', backupCount=0, interval=1)
        LogWriter.fileHandler.setFormatter(LogWriter.formatter)
        LogWriter.log.addHandler(LogWriter.fileHandler)

    @staticmethod
    def remove_log_file():
        LogWriter.log.removeHandler(LogWriter.fileHandler)
