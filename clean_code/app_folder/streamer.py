from dataclasses import dataclass, field
from loguru import logger
import cv2

@dataclass
class VideoStreamer:
    cap: cv2.VideoCapture = field(default=None, init=False)

    def start_stream(self):
        """Starts the camera stream."""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            logger.error("Kamera acilamadi!")
            raise Exception("Kamera acilamadi!")
        
        logger.info("Kamera basariyla acildi.")
        return self.cap

    def stop_stream(self):
        """Stops the camera stream and frees up resources."""
        if self.cap:
            self.cap.release()
            logger.info("Kamera basariyla kapatildi.")
