import tkinter as tk
from HeadLight_ExtractFrames_Buttons import VideoPlayer

def main():
    root = tk.Tk()
    root.title("Video Player")

    # Provide the path to your video file
    video_path = "./Video/Car_Video.mp4"

    player = VideoPlayer(root, video_path)

    root.mainloop()

if __name__ == "__main__":
    main()
