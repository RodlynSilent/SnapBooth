import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

class VideoApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        # Video capture
        self.cap = cv2.VideoCapture(1)
        if not self.cap.isOpened():
            raise ValueError("Unable to open video source")

        # Default filter is 'Normal'
        self.current_filter = 'Normal'

        # Canvas for video
        self.canvas = tk.Canvas(window, width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), 
                                height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        # Buttons for filters and capture
        self.create_buttons()

        # To save the last processed frame for capturing
        self.last_frame = None

        # Update & delay
        self.delay = 15   # milliseconds
        self.update()

        # Handle closing the window
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.window.mainloop()

    def create_buttons(self):
        filters = ['Normal', 'Sepia', 'Noir', 'Comic', 'Vintage', 'BMW']
        for filter_name in filters:
            btn = tk.Button(self.window, text=filter_name, width=10, command=lambda f=filter_name: self.set_filter(f))
            btn.pack(side=tk.LEFT)
        
        self.btn_capture = tk.Button(self.window, text="Capture", width=10, command=self.capture_frame)
        self.btn_capture.pack(side=tk.LEFT)

    def set_filter(self, filter_name):
        self.current_filter = filter_name

    def apply_filter(self, frame):
        if self.current_filter == 'Sepia':
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.array(frame, dtype=np.float64)
            frame = cv2.transform(frame, np.array([[0.393, 0.769, 0.189],
                                                  [0.349, 0.686, 0.168],
                                                  [0.272, 0.534, 0.131]]))
            frame = np.clip(frame, 0, 255)
            frame = np.array(frame, dtype=np.uint8)
        elif self.current_filter == 'Noir':
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            hsv[:, :, 2] = hsv[:, :, 2] * 0.5
            frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        elif self.current_filter == 'Comic':
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            frame = cv2.bitwise_and(frame, frame, mask=edges)
        elif self.current_filter == 'Vintage':
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            frame[:, :, 1] = frame[:, :, 1] * 0.8
            frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
            noise = np.random.randn(*frame.shape) * 10
            frame = np.clip(frame + noise, 0, 255).astype(np.uint8)
        elif self.current_filter == 'BMW':
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.last_frame = frame
        return frame

    def update(self):
        # Get a frame from the video source
        ret, frame = self.cap.read()

        if ret:
            # Apply selected filter
            frame = self.apply_filter(frame)

            # Convert image for tkinter
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def capture_frame(self):
        if self.last_frame is not None:
            # Save the processed frame
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                Image.fromarray(cv2.cvtColor(self.last_frame, cv2.COLOR_BGR2RGB)).save(file_path)

    def on_closing(self):
        # When everything is done, release the capture
        if self.cap.is_opened():
            self.cap.release()
        cv2.destroyAllWindows()
        self.window.destroy()

# Example usage
if __name__ == "__main__":
    app = VideoApp(tk.Tk(), "SnapBooth")

while True:
    # Capture frame-by-frame
    ret, frame = self.cap.read()

    # Display the resulting frame
    cv2.imshow('SnapBooth', frame)

    # If 'q' is pressed on the keyboard, break the loop and close the window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, call the on_closing method
self.on_closing()

