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
        self.cap = cv2.VideoCapture(0)  # Change to index 0 for default camera
        if not self.cap.isOpened():
            raise ValueError("Unable to open video source")

        # Default filter is 'Normal' and mirroring enabled
        self.current_filter = 'Normal'
        self.mirror = True  # Add flag for mirroring

        # Flags to control the update loop and window closing
        self.running = True
        self.closing = False

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
        
        # Add a button to toggle mirroring
        self.btn_mirror = tk.Button(self.window, text="Mirror", width=12, command=self.toggle_mirror)
        self.btn_mirror.pack(side=tk.LEFT)

    def set_filter(self, filter_name):
        self.current_filter = filter_name

    def apply_sepia(self, frame, intensity=0.5):
        # Verify alpha channel in the frame
        def verify_alpha_channel(frame):
            # If the frame does not have an alpha channel, add one
            if frame.shape[2] == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
            return frame

        frame = verify_alpha_channel(frame)
        frame_h, frame_w, frame_c = frame.shape
        sepia_bgra = (20, 66, 112, 1)
        overlay = np.full((frame_h, frame_w, 4), sepia_bgra, dtype='uint8')
        cv2.addWeighted(overlay, intensity, frame, 1.0, 0, frame)
        return frame

    def apply_filter(self, frame):
        if self.current_filter == 'Sepia':
            frame = self.apply_sepia(frame, intensity=0.5)  
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
        
        # Store the last frame
        self.last_frame = frame
        return frame


    def update(self):
        # Only update if running flag is True and not closing
        if self.running and not self.closing:
            # Get a frame from the video source
            ret, frame = self.cap.read()

            if ret:
                # Apply selected filter
                frame = self.apply_filter(frame)

                # Apply mirroring if necessary
                if self.mirror:
                    frame = cv2.flip(frame, 1)  # Flip the frame horizontally

                # Convert image for tkinter
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

            self.window.after(self.delay, self.update)  # Call update again after the delay


    def toggle_mirror(self):
        # Toggle the mirroring flag
        self.mirror = not self.mirror

    def capture_frame(self):
        if self.last_frame is not None:
            # Apply mirroring to the frame if necessary
            if self.mirror:
                frame_to_save = cv2.flip(self.last_frame, 1)  # Flip the frame horizontally
            else:
                frame_to_save = self.last_frame
            
            # Save the processed frame
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                Image.fromarray(cv2.cvtColor(frame_to_save, cv2.COLOR_BGR2RGB)).save(file_path)

    def on_closing(self):
        # Stop the update loop and set the closing flag
        self.running = False
        self.closing = True
        
        # When everything is done, release the capture
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        
        # Destroy the Tkinter window
        self.window.destroy()

# Example usage
if __name__ == "__main__":
    app = VideoApp(tk.Tk(), "SnapBooth")
