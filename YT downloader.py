from tkinter import *
from tkinter import filedialog
from pytube import YouTube

def download_video():
    link = entry.get()
    try:
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
        ys.download(output_folder)
        download_label.config(text="Download completed!!")
    except Exception as e:
        download_label.config(text="Error: " + str(e))

def select_output_folder():
    output_folder = filedialog.askdirectory()
    download_label.config(text="Show Output folder >> " + output_folder)

# Create the main window
window = Tk()
window.title("YouTube Downloader")

# Create and place widgets in the window
label = Label(window, text="Enter the link of YouTube video:")
label.pack(pady=10)

entry = Entry(window, width=40)
entry.pack(pady=10)

download_button = Button(window, text="Download", command=download_video)
download_button.pack(pady=10)

output_folder_button = Button(window, text="Show Output Folder", command=select_output_folder)
output_folder_button.pack(pady=10)

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
