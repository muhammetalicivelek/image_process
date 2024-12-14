from loguru import logger
import os

class LogManager:
    def __init__(self, log_dir="logs_folder", log_file_name="app.log", level="INFO", rotation="10 MB", compression="zip"):
        """
        Log dosyasını ve logger yapılandırmasını yönetir.

        Args:
            log_dir (str): Log dosyasının saklanacağı dizin.
            log_file_name (str): Log dosyasının adı.
            level (str): Log seviyesini belirler (INFO, DEBUG, ERROR, vb.).
            rotation (str): Log dosyası boyutu veya zamana bağlı rotasyon (örn. '10 MB', '1 day').
            compression (str): Log dosyasını sıkıştırma yöntemi (örn. 'zip', 'tar').
        """
        self.log_dir = log_dir
        self.log_file_name = log_file_name
        self.log_file_path = os.path.join(self.log_dir, self.log_file_name)
        self.level = level
        self.rotation = rotation
        self.compression = compression

        self._setup_logger()

    def _setup_logger(self):
        """Logger yapılandırmasını oluşturur."""
        # Log dizinini oluştur
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Varsayılan logger'ı kaldır
        logger.remove()

        # Logger ayarlarını yapılandır
        logger.add(
            self.log_file_path,
            format="{time} | {level} | {module}:{line} | {message}",
            mode="w",
            level=self.level,
            rotation=self.rotation,
            compression=self.compression
        )

    def get_logger(self):
        """Logger nesnesini döndürür."""
        return logger







