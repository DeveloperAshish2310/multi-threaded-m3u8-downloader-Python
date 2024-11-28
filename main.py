import os
import requests
import subprocess
import re
from concurrent.futures import ThreadPoolExecutor

# Step 1: Read the m3u8 file to extract the segment URLs using regex

# Function to read the m3u8 file and extract segment URLs
def get_m3u8_urls(m3u8_url_or_path):
    # If the m3u8 file is hosted online (URL)
    if m3u8_url_or_path.startswith("http"):
        response = requests.get(m3u8_url_or_path)
        response.raise_for_status()  # Raise an error if the request fails
        m3u8_content = response.text
    else:
        # If the m3u8 file is local (path)
        with open(m3u8_url_or_path, 'r') as file:
            m3u8_content = file.read()
    
    # Regex pattern to extract URLs (including both m3u8 and .ts files)
    url_pattern = re.compile(r'(https?://[^\s]+)')
    
    # Find all matching URLs in the m3u8 content
    urls = url_pattern.findall(m3u8_content)
    
    return urls


# Step 2: Function to download each video segment
def download_segment(url, segment_file):
    print(f"Downloading {url}...")
    response = requests.get(url)
    with open(segment_file, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {url} to {segment_file}")


# Step 3: Main function to download all segments concurrently and merge them
def download_and_merge_video(m3u8_file, num_threads=4):
    # Step 3.1: Get segment URLs from the m3u8 file
    urls = get_m3u8_urls(m3u8_file)
    
    # Step 3.2: Create a temporary directory to store the segments
    temp_dir = 'temp_segments'
    os.makedirs(temp_dir, exist_ok=True)

    # Step 3.3: Prepare a list of future tasks to download each segment
    downloaded_files = []
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit download tasks for each segment
        for idx, url in enumerate(urls):
            segment_file = os.path.join(temp_dir, f"segment_{idx}.ts")
            future = executor.submit(download_segment, url, segment_file)
            downloaded_files.append(segment_file)

    # Step 3.4: Create the concat list file with absolute paths
    concat_file = os.path.join(temp_dir, 'concat_list.txt')

    # Create a file listing all segment files with absolute paths
    with open(concat_file, 'w') as f:
        for segment in downloaded_files:
            f.write(f"file '{os.path.abspath(segment)}'\n")

    # Step 3.5: Combine the downloaded segments using ffmpeg
    output_file = "output_video.mp4"

    # Run ffmpeg to combine the segments into one video
    print("Merging segments into final video...")

    # -- FFMPEG Do not re-encode the video
    subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_file, '-c', 'copy', output_file])
    
    # -- Force ffmpeg to Re-encode the Video
    # subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_file, '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental', output_file])

    # -- Force ffmpeg to Handle Timestamps Properly:
    # subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_file, '-fflags', '+genpts', '-c', 'copy', output_file])

    # Step 3.6: Cleanup: remove temporary files
    print("Cleaning up temporary files...")
    for file in downloaded_files:
        os.remove(file)
    os.remove(concat_file)

    print(f"Video saved as {output_file}")


# Example usage: Provide the m3u8 file URL or local file path and the number of threads
m3u8_file = 'video_playlist.m3u8'
num_threads = 10  # Set the number of threads to use
download_and_merge_video(m3u8_file, num_threads)
