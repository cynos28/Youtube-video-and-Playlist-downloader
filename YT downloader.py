
from pytube import Playlist
from pytube import YouTube

print("<--------------------- Created by Cynos28 ------------------->")
# Gives download progress
def on_progress(stream, chunk, bytes_remaining):
    progress = f"{round(100 - (bytes_remaining / stream.filesize * 100), 2)}%"
    print(f"progress: {progress}")


# Do this on download completion
def on_complete(stream, file_path):
    print("Download Completed")
    print(f"Download path: {file_path}")


# get playlist url from user
pl_url = input("Please enter Playlist URL:\n")

# Create Playlist obj
pl = Playlist(pl_url)

# Num of videos in playlist
video_count = pl.length
remaining_video_count = 0

print(f"Number of videos in the playlist: {video_count}")
print("Downloading started...")

# for every video in the playlist
for vids in pl.videos:

    vid_url = vids.watch_url
    yt = YouTube(url=vid_url, on_progress_callback=on_progress, on_complete_callback=on_complete)  # create Youtube obj

    res_1080p = yt.streams.get_by_resolution('1080p')
    res_480p = yt.streams.get_by_resolution('480p')
    res_720p = yt.streams.get_by_resolution('720p')
    res_360p = yt.streams.get_by_resolution('360p')

    if res_480p and yt.streams.filter(file_extension='mp4', progressive=True):  # if the resolution match 480p
        title = yt.title
        print(f"Video title: {title}")
        print("Video download quality: 480p")
        file_size = round((res_480p.filesize / 1000000), 2)
        print(f"File Size: {file_size} MB")
        res_480p.download()
        remaining_video_count += 1
        print("\n")

    elif res_1080p and yt.streams.filter(file_extension='mp4', progressive=True):  # if the resolution match 1080p
        title = yt.title
        print(f"Video title: {title}")
        print("Video download quality: 360p")
        file_size = round((res_1080p.filesize / 1000000), 2)
        print(f"File Size: {file_size} MB")
        res_1080p.download()
        remaining_video_count += 1
        print("\n")

    elif res_720p and yt.streams.filter(file_extension='mp4', progressive=True):  # if the resolution match 720p
        title = yt.title
        print(f"Video title: {title}")
        print("Video download quality: 720p")
        file_size = round((res_720p.filesize / 1000000), 2)
        print(f"File Size: {file_size} MB")
        res_720p.download()
        remaining_video_count += 1
        print("\n")

    elif (res_360p and yt.streams.filter(file_extension='mp4', progressive=True)):  # if the resolution match 360p
        title = yt.title
        print(f"Video title: {title}")
        print("Video download quality: 360p")
        file_size = round((res_360p.filesize / 1000000), 2)
        print(f"File Size: {file_size} MB")
        res_360p.download()
        remaining_video_count += 1
        print("\n")

    else:
        print("Low quality video. No video will be downloaded")

    print(f"Remaining: {remaining_video_count} out of {video_count}")



