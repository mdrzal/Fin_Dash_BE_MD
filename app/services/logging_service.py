import logging

class LoggingService:
    @staticmethod
    def get_logger(name: str = None):
        logger = logging.getLogger(name if name else __name__)
        if not logger.hasHandlers():
            logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s [%(name)s]: %(message)s')
        return logger
