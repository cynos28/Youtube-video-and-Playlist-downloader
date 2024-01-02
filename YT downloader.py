from tkinter import *
from tkinter import filedialog
from pytube import YouTube, Playlist

def on_progress(stream, chunk, bytes_remaining):
    progress = f"{round(100 - (bytes_remaining / stream.filesize * 100), 2)}%"
    print(f"progress: {progress}")

def on_complete(stream, file_path):
    print("Download Completed")
    print(f"Download path: {file_path}")

def download_single_video():
    link = entry.get()
    try:
        yt = YouTube(link)
        output_folder = filedialog.askdirectory()

        title_label.config(text="Title: " + yt.title)
        views_label.config(text="Number of views: " + str(yt.views))
        length_label.config(text="Length of video: " + str(yt.length))
        rating_label.config(text="Rating of video: " + str(yt.rating))
        download_label.config(text="Downloading to: " + output_folder)

        ys = yt.streams.get_highest_resolution()
        ys.download(output_folder)
        download_label.config(text="Download completed!!")
    except Exception as e:
        download_label.config(text="Error: " + str(e))

def download_playlist():
    pl_url = playlist_entry.get()
    pl = Playlist(pl_url)
    video_count = pl.length
    remaining_video_count = 0

    for vid in pl.videos:
        yt = YouTube(url=vid.watch_url, on_progress_callback=on_progress, on_complete_callback=on_complete)

        resolutions = ['1080p', '720p', '480p', '360p']
        for resolution in resolutions:
            stream = yt.streams.get_by_resolution(resolution)
            if stream and yt.streams.filter(file_extension='mp4', progressive=True):
                title = yt.title
                print(f"Video title: {title}")
                print(f"Video download quality: {resolution}")
                file_size = round((stream.filesize / 1000000), 2)
                print(f"File Size: {file_size} MB")
                stream.download()
                remaining_video_count += 1
                print("\n")
                break  # Break after the first successful download

    print(f"Remaining: {remaining_video_count} out of {video_count}")

# Create the main window
window = Tk()
window.title("YouTube Downloader")

# Create and place widgets in the window
single_video_label = Label(window, text="Enter the link of YouTube video:")
single_video_label.pack(pady=10)

entry = Entry(window, width=40)
entry.pack(pady=10)

single_video_button = Button(window, text="Download Single Video", command=download_single_video)
single_video_button.pack(pady=10)

playlist_label = Label(window, text="Enter the URL of YouTube playlist:")
playlist_label.pack(pady=10)

playlist_entry = Entry(window, width=40)
playlist_entry.pack(pady=10)

playlist_button = Button(window, text="Download Playlist", command=download_playlist)
playlist_button.pack(pady=10)

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

# Start the GUI event loop
window.mainloop()
