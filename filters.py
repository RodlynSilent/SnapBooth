import cv2
import numpy as np

class Filters:
    def __init__(self):
        pass

    def grayscale(self, frame):
        """Converts the frame to grayscale."""
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def sepia(self, frame):
        """Applies a sepia filter to the frame."""
        kernel = np.array([
            [.393, .769, .189],
            [.349, .686, .168],
            [.272, .534, .131]
        ])
        return cv2.transform(frame, kernel)

    def noir(self, frame):
        """Applies a noir filter to the frame (increased contrast and shadows)."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (21, 21), 0)
        canny = cv2.Canny(blurred, 0, 100)
        return cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)

# Add more
