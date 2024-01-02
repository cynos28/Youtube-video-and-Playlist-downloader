from tkinter import *
from tkinter import filedialog
from pytube import YouTube, Playlist
import webbrowser

def on_progress(stream, chunk, bytes_remaining):
    global current_video_title
    progress = f"{round(100 - (bytes_remaining / stream.filesize * 100), 2)}%"
    update_status(f"Progress for {current_video_title}: {progress}")

def on_complete(stream, file_path):
    update_status("Download Completed")
    update_status(f"Download path: {file_path}")

def update_status(new_status):
    download_text.configure(state='normal')
    download_text.insert(END, new_status + "\n")
    download_text.configure(state='disabled')
    download_text.see(END)  # Automatically scroll to the bottom

def download_single_video():
    link = entry.get()
    try:
        yt = YouTube(link, on_progress_callback=on_progress, on_complete_callback=on_complete)
        output_folder = filedialog.askdirectory()

        title_label.config(text="Title: " + yt.title)
        views_label.config(text="Number of views: " + str(yt.views))
        length_label.config(text="Length of video: " + str(yt.length))
        rating_label.config(text="Rating of video: " + str(yt.rating))
        update_status(f"Downloading {yt.title} to: {output_folder}")
        global current_video_title
        current_video_title = yt.title

        ys = yt.streams.get_highest_resolution()
        ys.download(output_folder)
        update_status("Download completed!!")
    except Exception as e:
        update_status("Error: " + str(e))

def download_playlist():
    pl_url = playlist_entry.get()
    pl = Playlist(pl_url)
    output_folder = filedialog.askdirectory()

    total_video_count = pl.length
    remaining_video_count = 0

    total_videos_label.config(text=f"Total Videos: {total_video_count}")

    for vid in pl.videos:
        global current_video_title
        current_video_title = vid.title
        yt = YouTube(url=vid.watch_url, on_progress_callback=on_progress, on_complete_callback=on_complete)

        resolutions = ['1080p', '720p', '480p', '360p']
        for resolution in resolutions:
            stream = yt.streams.get_by_resolution(resolution)
            if stream and yt.streams.filter(file_extension='mp4', progressive=True):
                title = yt.title
                update_status(f"Downloading {title} to: {output_folder}")
                stream.download(output_folder)
                remaining_video_count += 1
                update_status(f"Downloaded {title} to: {output_folder}")
                break  # Break after the first successful download

    update_status(f"Remaining: {remaining_video_count} out of {total_video_count}")

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

total_videos_label = Label(window, text="")
total_videos_label.pack()

download_text = Text(window, height=10, width=60, wrap=WORD)
download_text.pack(pady=10)
download_text.configure(state='disabled')

# Add label for creator's information and hyperlink
creator_label = Label(window, text="Created by Cynos28")
creator_label.pack(pady=5)
creator_label.bind("<Button-1>", lambda event: webbrowser.open("https://github.com/cynos28"))
creator_label.config(cursor="hand2", fg="blue", underline=True)

# Global variable to store the current video title
current_video_title = ""

# Start the GUI event loop
window.mainloop()
