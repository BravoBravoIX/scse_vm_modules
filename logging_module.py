import logging
from logging.handlers import RotatingFileHandler

class LoggingModule:
    def __init__(self, log_file='system.log', log_level=logging.INFO):
        """
        Initialize the logging module with the specified log file and log level.
        """
        self.log_file = log_file
        self.log_level = log_level
        self.setup_logging()
    
    def setup_logging(self):
        """
        Set up the logging configuration.
        """
        handler = RotatingFileHandler(self.log_file, maxBytes=5*1024*1024, backupCount=5)
        logging.basicConfig(level=self.log_level,
                            format='%(asctime)s %(levelname)s: %(message)s',
                            handlers=[handler])
    
    def log(self, level, message):
        """
        Log a message with the specified level.
        """
        if level == 'debug':
            logging.debug(message)
        elif level == 'info':
            logging.info(message)
        elif level == 'warning':
            logging.warning(message)
        elif level == 'error':
            logging.error(message)
        elif level == 'critical':
            logging.critical(message)
        else:
            logging.info(message)

# Example usage:
if __name__ == "__main__":
    logger = LoggingModule()
    logger.log('info', 'This is an info message.')
    logger.log('error', 'This is an error message.')
