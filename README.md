# M3U8 Video Downloader and Merger

This Python script downloads video segments from an M3U8 playlist, processes them in parallel using multiple threads, and then merges them into a single video file. It uses the `requests`, `concurrent.futures`, and `ffmpeg` libraries.

## Features

- **Multithreaded Download**: Downloads multiple video segments concurrently to speed up the process.
- **Flexible Thread Count**: Allows you to set the number of threads for concurrent downloads.
- **FFmpeg Concatenation**: Merges downloaded segments into a single video file using `ffmpeg`.
- **Customizable**: Accepts both remote M3U8 URLs and local M3U8 file paths.

## Requirements

Before using the script, make sure to install the required dependencies:

- Python 3.x
- `requests`: To download video segments.
- `ffmpeg`: To merge video segments.

### Install Dependencies

You can install the required Python libraries by running:

```bash
pip install requests
```

You also need to install `ffmpeg`. On most systems, you can install it using the following:

#### Windows:
Download `ffmpeg` from [FFmpeg's official website](https://ffmpeg.org/download.html) and add it to your system's `PATH`.

#### macOS (Homebrew):
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install ffmpeg
```

## Usage

1. **Download the script** to your local machine.
2. **Edit the script**:
   - Set the `m3u8_file` variable to either a URL or a local file path of your M3U8 playlist.
   - Optionally set the `num_threads` variable to control how many threads will be used for downloading segments.

Example:

```python
m3u8_file = 'https://example.com/path/to/playlist.m3u8'  # Replace with your M3U8 URL or file path
num_threads = 4  # Set the number of threads to use for parallel downloading
```

3. **Run the script**:

   ```bash
   python m3u8_downloader.py
   ```

The script will:
- Download all segments listed in the M3U8 playlist concurrently.
- Merge the downloaded segments into a single MP4 file named `output_video.mp4`.
- Clean up temporary files after the process is complete.

### Example Command

```bash
python m3u8_downloader.py
```

## Parameters

- **`m3u8_file`**: The URL or local file path of the M3U8 playlist.
- **`num_threads`**: Number of threads to use for parallel downloading. Default is 4.

## How It Works

1. **Extracts Segment URLs**: The script extracts all segment URLs from the M3U8 playlist using a regular expression.
2. **Downloads Segments**: It uses Python's `requests` library to download video segments. Downloads are done concurrently using the `ThreadPoolExecutor` for better performance.
3. **Merges Segments**: The downloaded `.ts` segments are merged into a single video file using `ffmpeg`.
4. **Cleans Up**: Temporary files are deleted after merging.

## Troubleshooting

### 1. Non-monotonic DTS Warning

If you encounter a warning related to "Non-monotonic DTS", you can try forcing `ffmpeg` to re-encode the video, which will reprocess the timestamps. Modify the `subprocess.run` command in the script:

```python
subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_file, '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental', output_file])
```

This forces `ffmpeg` to re-encode both the video and audio, ensuring that the timestamps are consistent and resolving the warning.

### 2. Slow Downloads

If downloading is too slow, try increasing the number of threads (`num_threads`). Note that increasing the number of threads too much might overwhelm your network, so find a balance that works for your connection.

### 3. Segment Order Issues

Make sure the M3U8 playlist and its segments are in correct order. If you encounter problems with segment ordering, verify that the playlist is correctly formatted, and that no segments are missing.

## License

This project is licensed under the MIT License.