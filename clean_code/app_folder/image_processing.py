from dataclasses import dataclass, field
import cv2
import numpy as np
from streamer import VideoStreamer
from config import Config 

@dataclass
class ColorRange:
    lower: tuple
    upper: tuple

@dataclass
class ColorObjectDetector:
    color_ranges: dict = field(default_factory=dict)

    def __post_init__(self):
        # Config dosyasından renk aralıklarını alıyoruz
        config = Config()
        color_config = config.get_config("colors")
        self.color_ranges = {
            color_name: ColorRange(tuple(color_range[0]), tuple(color_range[1]))
            for color_name, color_range in color_config.items()
        }

    def detect_objects_with_color(self, frame):
        """Detect objects of specific colors and draw circles around them with color labels."""
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        for color_name, color_range in self.color_ranges.items():
            lower_bound = np.array(color_range.lower, dtype=np.uint8)
            upper_bound = np.array(color_range.upper, dtype=np.uint8)

            # Create mask
            mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)

            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 500:  # Minimum area threshold
                    (x, y), radius = cv2.minEnclosingCircle(contour)
                    center = (int(x), int(y))
                    radius = int(radius)
                    cv2.circle(frame, center, radius, (0, 255, 255), 2)
                    cv2.putText(frame, color_name, (center[0] - 10, center[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        return frame

    def process_frame(self, frame):
        """Process the frame to detect objects and display their colors."""
        return self.detect_objects_with_color(frame)

if __name__ == "__main__":
    # VideoStreamer sınıfını kullanarak video akışını başlat
    streamer = VideoStreamer()
    cap = streamer.start_stream()

    detector = ColorObjectDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        processed_frame = detector.process_frame(frame)
        cv2.imshow("Processed Video Stream", processed_frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC tuşu ile çıkış
            break

    streamer.stop_stream()
    cv2.destroyAllWindows()


