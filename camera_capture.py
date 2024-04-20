import tkinter as tk
import cv2
from PIL import Image, ImageTk
import os
from filters import Filters  # Import the Filters class

class Webcam:
    def __init__(self, root):
        self.root = root
        self.root.title("SnapBooth")  # Set the title of the application

        # Create a frame to hold all the camera grids
        self.camera_frame = tk.Frame(root)
        self.camera_frame.pack()

        # Define the number of rows and columns for the camera grids
        self.rows = 1
        self.cols = 3

        # Create a list to store the video capture objects and canvas widgets
        self.cameras = []
        self.canvases = []
        self.selected_filter = tk.StringVar(root)
        self.selected_filter.set("Normal")

        # Create filters for each camera grid (including new filter names)
        self.filters = ["Normal", "Sepia", "Noir"] * (self.rows * self.cols)

        # Create video capture objects and canvas widgets for each grid
        for i in range(self.rows):
            for j in range(self.cols):
                # Create a video capture object (using DSHOW backend)
                cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

                # Create a canvas widget to display the webcam feed
                canvas = tk.Canvas(self.camera_frame, width=300, height=200)
                self.canvases.append(canvas)
                canvas.grid(row=i, column=j, padx=5, pady=5)

                # Add the capture object and canvas to the lists
                self.cameras.append(cap)

        # Create a frame to hold the filter buttons
        self.filter_frame = tk.Frame(root)
        self.filter_frame.pack()

        # Define filter buttons with lambda functions for efficient binding
        self.filter_buttons = {}
        for filter_name in self.filters:
            button = tk.Button(self.filter_frame, text=filter_name,
                          command=lambda f=filter_name: self.set_filter(f))
            button.pack(side=tk.LEFT, padx=5)
            self.filter_buttons[filter_name] = button

        # Button to capture images from all grids
        self.capture_button = tk.Button(root, text="Capture Images", command=self.capture_images)
        self.capture_button.pack()

        # Call the main loop to start the application
        self.main()
    
    def set_filter(self, filter_name):
        self.selected_filter.set(filter_name)
    
    def apply_filter(self, filter_name, grid_index):
        # Update button selection (optional, visual feedback)
        for name, button in self.filter_buttons.items():
            button.config(relief=tk.RAISED if name == filter_name else tk.FLAT)

        # Set the selected filter for the specified grid
        self.filters[grid_index] = filter_name

    def main(self):
        while True:
            # Capture frames from all cameras
            frames = []
            for cap in self.cameras:
                ret, frame = cap.read()
                if not ret:
                    print("Error! Unable to capture frame")
                    break
                frames.append(frame)

            if not frames:
                break

            # Convert frames to RGB format (OpenCV uses BGR)
            rgb_frames = [cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) for frame in frames]

            # Create PIL images and PhotoImage objects for each frame
            images = [Image.fromarray(rgb_frame) for rgb_frame in rgb_frames]
            imgtks = [ImageTk.PhotoImage(image=image) for image in images]

            # Update the canvas widgets with the new images and filters
            for i, (canvas, imgtk) in enumerate(zip(self.canvases, imgtks)):
                canvas.delete("all")

                # Apply filter if selected for this grid
                filtered_frame = rgb_frames[i]
                if self.filters[i] != "Normal":
                    filters = Filters()
                    filtered_frame = getattr(filters, self.filters[i].lower().replace(" ", "_"))(filtered_frame)

                # Update the canvas widget with the filtered image
                canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)

            # Update the window to display the new frames
            self.root.update()

    def capture_images(self):
        # Get current date and time
        current_time = str(os.path.getctime("."))[:10]

        # Capture and save images from all grids
        for i, (cap, filter_name) in enumerate(zip(self.cameras, self.filters)):
            ret, frame = cap.read()

            # Apply filter if selected for this grid
            if filter_name != "Normal":
                filters = Filters()
                filtered_frame = getattr(filters, filter_name.lower().replace(" ", "_"))(frame)
            else:
                filtered_frame = frame

            # Save the image to the Downloads directory
            cv2.imwrite(f"C:/Users/rodsi/Downloads/webcam_image_{current_time}_{i}.jpg", filtered_frame)

        print("Images captured and saved successfully!")

# Create the main window
root = tk.Tk()

# Create an instance of the Webcam class
webcam = Webcam(root)

# Start the application
root.mainloop()

