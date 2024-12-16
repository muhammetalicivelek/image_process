import sys
import os
# app_folder dizinini PYTHONPATH'e ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app_folder')))

import cv2
from app_folder.config import Config
from app_folder.image_processing import ColorObjectDetector
from app_folder.streamer import VideoStreamer
from app_folder.logger import LogManager

class ImageProcessingApp:
    def __init__(self):
        """Initialize application components."""
        
        self.logger = LogManager().get_logger()
        self.logger.info("log sistemi baslatildi.")
        self.config_manager = Config()
        self.detector = ColorObjectDetector()
        self.streamer = VideoStreamer()
        self.cap = None

        self._load_config()

    def _load_config(self):
        """Load the configuration file."""
        self.config_manager.load_config()
        self.logger.info("config dosyasi yuklendi")
    
    def start_processing(self):
        """Start the image processing process."""
        self.logger.info("Görüntü işleme baslatildi")

        self.cap = self.streamer.start_stream()

        if not self.cap.isOpened():
            self.logger.error("Kamera baslatilamadi.")
            return

        while True:
            ret, frame = self.cap.read()
            if not ret:
                self.logger.error("Kare yakalanamadi, cikiliyor...")
                break

            # Renk algılama ve işleme
            processed_frame = self.detector.process_frame(frame)

            cv2.imshow("Processed Video Stream", processed_frame)

            if cv2.waitKey(1) & 0xFF == 27:
                self.logger.info("Goruntu isleme durduruldu.")
                break

        # Kaynakları serbest bırak
        self.stop_processing()

    def stop_processing(self):
        """Free up resources and close windows."""
        if self.cap:
            self.streamer.stop_stream()
        cv2.destroyAllWindows()
        self.logger.info("Kaynaklar serbest birakildi ve pencereler kapatildi.")

if __name__ == "__main__":
    app = ImageProcessingApp()
    app.start_processing()


