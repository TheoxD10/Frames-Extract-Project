import os
import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk

# brief description:
# def __init__(self, master, video_path): - creates a GUI
# parameters:
# self: The conventional name for the instance of the class.
# master: This parameter is an instance of the Tkinter Tk class or any other Tkinter widget.
# It represents the main window or the parent widget where the video player will be embedded.
# video_path: This parameter represents the path to the video file that the player will load and play.

class VideoPlayer:
    def __init__(self, master, video_path):
        self.master = master
        self.video_path = video_path
        self.vidcap = cv2.VideoCapture(self.video_path)
        self.success, self.image = self.vidcap.read()
        self.paused = False
        self.current_frame = 0

        self.canvas = tk.Canvas(master, width=self.vidcap.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_rewind = tk.Button(master, text="Rewind", command=self.rewind, width=10, height=2, font=('Helvetica', 14))
        self.btn_rewind.pack(side=tk.LEFT)

        self.btn_pause = tk.Button(master, text="Pause/Unpause", command=self.toggle_pause, width=15, height=2, font=('Helvetica', 14))
        self.btn_pause.pack(side=tk.LEFT)

        self.btn_forward = tk.Button(master, text="Forward", command=self.forward, width=10, height=2, font=('Helvetica', 14))
        self.btn_forward.pack(side=tk.LEFT)

        self.extract_frames_button = tk.Button(master, text="Extract Frames", command=self.extract_frames, width=15, height=2, font=('Helvetica', 14))
        self.extract_frames_button.pack(side=tk.RIGHT)

        self.update()

# brief description:
# the rewind method in the VideoPlayer class is responsible for rewinding the video playback by a specified duration,
# assuming a frame rate of 30 frames  second

    def rewind(self):
        # Rewind by 2 seconds (assuming 30 frames per second)
        forwardTimeinSeconds = 2
        fps = 30
        target_frame = max(0, self.current_frame - forwardTimeinSeconds * fps)
        self.vidcap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
        self.current_frame = target_frame

# brief description:
# the pause method in the VideoPlayer class is responsible for pausing the video (self)
    def toggle_pause(self):

        self.paused = not self.paused

# brief description:
# the forward method in the VideoPlayer class is responsible for forwarding the video playback by a specified duration,
# assuming a frame rate of 30 frames second

    def forward(self):
        # Forward by 2 seconds (assuming 30 frames per second)
        forwardTimeinSeconds = 2
        fps = 30
        target_frame = min(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT) - 1, self.current_frame + forwardTimeinSeconds * fps)
        self.vidcap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
        self.current_frame = target_frame

# brief description:
# the extract_frames method in the VideoPlayer class is responsible for extracting frames from the video and
# saving them as individual image files in a specified directory.
    def extract_frames(self):

        vidcap = cv2.VideoCapture(self.video_path)
        success, image = vidcap.read()

        count = 0
        while success:
            cv2.imwrite(f"./Frames/frame_{count}.png", image)
            count += 1
            success, image = vidcap.read()

        vidcap.release()
        print("Frames extracted successfully.")

# brief description:
# the update method in the VideoPlayer class is responsible for updating the display of video frames in
# the Tkinter canvas.
    def update(self):
        if not self.paused:
            self.success, self.image = self.vidcap.read()
            self.current_frame += 1

        if self.success:
            photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)))
            self.canvas.config(width=photo.width(), height=photo.height())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo

        if not self.success:
            self.btn_rewind.destroy()
            self.btn_pause.destroy()
            self.btn_forward.destroy()
            self.extract_frames_button.destroy()
            self.canvas.destroy()
        miliseconds=25
        self.master.after(miliseconds, self.update)
# brief description:
# the __del__ method in the VideoPlayer class is a destructor method, and it is automatically called when
# an object is about to be destroyed or deallocated. In this case, it releases the OpenCV VideoCapture object to
# free up system resources.
    def __del__(self):
        self.vidcap.release()

