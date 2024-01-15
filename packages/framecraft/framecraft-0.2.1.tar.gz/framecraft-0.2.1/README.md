# 📷 framecraft
Framecraft is a library that translates video into frame images in multiprocessing.


## 🛠️ installation 
```
pip install frame craft
```

## 📚 example
```
import framecraft

video_path = "/path/to/videopath"
frames_dir = "/path/to/savepath"
framecraft.capture(video_path, frames_dir)

"""
framecraft.capture options
* video_path: path to the video  
* frames_dir: directory to save the frames
overwrite: overwrite frames if they exist?
every: extract every this many frames
chunk_size: how many frames to split into chunks (one chunk per cpu core process)
format : frames file format
"""
```
