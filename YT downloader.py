from tkinter import *
from tkinter import filedialog
from pytube import YouTube, Playlist
import threading

def download_video():
    link = entry.get()
    yt = YouTube(link)

    # Showing details in the GUI
    title_label.config(text="Title: " + yt.title)
    views_label.config(text="Number of views: " + str(yt.views))
    length_label.config(text="Length of video: " + str(yt.length))
    rating_label.config(text="Rating of video: " + str(yt.rating))

    # Choose output folder
    output_folder = filedialog.askdirectory()
    download_label.config(text="Downloading to: " + output_folder)

    # Getting the highest resolution possible
    ys = yt.streams.get_highest_resolution()

    # Starting download
    download_thread = threading.Thread(target=download_video_thread, args=(ys, output_folder))
    download_thread.start()

def download_video_thread(ys, output_folder):
    def on_progress(chunk, bytes_remaining, _):
        total_size = ys.filesize
        downloaded = total_size - bytes_remaining
        percent = (downloaded / total_size) * 100
        progress_label.config(text=f"Downloading... {percent:.2f}%")

    ys.register_on_progress_callback(on_progress)
    ys.download(output_folder)

    progress_label.config(text="Download completed!!")

def download_playlist():
    # get playlist url from user
    pl_url = entry.get()

    # Create Playlist obj
    pl = Playlist(pl_url)

    # Choose output folder for playlist
    output_folder = filedialog.askdirectory()
    download_label.config(text="Downloading to: " + output_folder)

    # Num of videos in playlist
    video_count = pl.length
    remaining_video_count = 0

    download_label.config(text=f"Number of videos in the playlist: {video_count}")
    download_label.update()

    # for every video in the playlist
    for index, vids in enumerate(pl.videos, start=1):
        vid_url = vids.watch_url
        yt = YouTube(url=vid_url)

        res_480p = yt.streams.get_by_resolution('480p')

        if res_480p and yt.streams.filter(file_extension='mp4', progressive=True):  # if the resolution match 480p
            title = yt.title
            download_label.config(text=f"Downloading video {index}/{video_count}: {title} - 480p")
            download_label.update()
            res_480p.download(output_folder)
            remaining_video_count += 1

        # ... (similar logic for other resolutions)

        else:
            download_label.config(text=f"Skipping video {index}/{video_count}: Low quality or no suitable stream")

        download_label.config(text=f"Remaining: {remaining_video_count} out of {video_count}")
        download_label.update()

# Create the main window
window = Tk()
window.title("YouTube Downloader")

# Create and place widgets in the window
label = Label(window, text="Enter the link of YouTube video or playlist:")
label.pack(pady=10)

entry = Entry(window, width=40)
entry.pack(pady=10)

download_button = Button(window, text="Download Video", command=download_video)
download_button.pack(pady=10)

download_playlist_button = Button(window, text="Download Playlist", command=download_playlist)
download_playlist_button.pack(pady=10)

title_label = Label(window, text="")
title_label.pack()

views_label = Label(window, text="")
views_label.pack()

length_label = Label(window, text="")
length_label.pack()

rating_label = Label(window, text="")
rating_label.pack()

download_label = Label(window, text="")
download_label.pack(pady=10)

progress_label = Label(window, text="")
progress_label.pack()

# Start the GUI event loop
window.mainloop()
