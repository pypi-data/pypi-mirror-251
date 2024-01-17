import logging , os , inspect
from datetime import datetime
from logging.handlers import RotatingFileHandler


class DEBUGGER:
    def __init__(self, name, level='info', onscreen=True,log_rotation=3,homePath=os.getcwd() ):
        self.logger = logging.getLogger(name)
        self.set_level(level)
        self.LOG_SIZE_THRESHOLD = 10 * 1024 * 1024
        self.BACKUP_COUNT = log_rotation
        self.homePath = homePath
        

        path = f"{self.homepath()}/debug/{name}.log"


        if not os.path.exists(f"{self.homepath()}/debug/") : 
            os.makedirs(f"{self.homepath()}/debug/")
            open(path , 'w').write('')
        

        # Create a formatter and add it to the handler
        f = f"[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s"
        formatter = logging.Formatter(f)

        # Create a file handler and set the formatter
        file_handler = RotatingFileHandler(path ,  maxBytes=self.LOG_SIZE_THRESHOLD , backupCount=self.BACKUP_COUNT )
        file_handler.setFormatter(formatter)


        # Create a stream handler and set the formatter
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(formatter)

        # Add the file handler to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(self.stream_handler)

        if onscreen : self.enable_print()
        elif not onscreen : self.disable_print()


    def change_log_size(self, size):
        self.LOG_SIZE_THRESHOLD = size
    
    def homepath(self) :
        return self.homePath

    def enable_print(self) :
        self.logger.addHandler(self.stream_handler)

    def disable_print(self) : 
         self.logger.removeHandler(self.stream_handler)


    def changeHomePath( self , path ) :
        self.homePath = path


    def set_level(self, level : str):
        if 'info' in level.lower() : lvl = logging.INFO
        elif 'warn' in level.lower() : lvl = logging.WARNING
        elif 'warning' in level.lower() : lvl = logging.WARNING
        elif 'critical' in level.lower() : lvl = logging.CRITICAL
        elif 'debug' in level.lower() : lvl = logging.DEBUG
        elif 'error' in level.lower() : lvl = logging.ERROR
        self.logger.setLevel(lvl)

    def get_logger(self) : 
        return self.logger

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


    def get_current_function(self):
        frame = inspect.currentframe().f_back.f_back
        function_name = frame.f_code.co_name
        # print(function_name)
        return function_name
    
