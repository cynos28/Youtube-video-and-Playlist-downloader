import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [Executable("YT-downloader.py", base=base, target_name="youtube_downloader.exe")]

build_exe_options = {
    "packages": ["tkinter", "pytube"],
    "include_files": [],
}

setup(
    name="YouTubeDownloader",
    version="1.0",
    description="YouTube Downloader",
    options={"build_exe": build_exe_options},
    executables=executables
)
