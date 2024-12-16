from loguru import logger

class LogManager:
    def __init__(self,log_file_name="logs_folder/app.log", level="INFO", rotation="10 MB"):
   
        self.log_file_name = log_file_name
        self.level = level
        self.rotation = rotation
        
        self._setup_logger()

    def _setup_logger(self):
        """Logger yapılandırmasını oluşturur."""
        
        logger.remove()

        logger.add(
            self.log_file_name,
            format="{time} | {level} | {module}:{line} | {message}",
            mode="w",
            level=self.level,
            rotation=self.rotation,
            )

    def get_logger(self):
        """Logger nesnesini döndürür."""
        return logger







