import subprocess
import json

def get_video_metadata(video_path):
    cmd = [
        "ffprobe", "-i", video_path,
        "-show_entries", "format=size,duration,bit_rate,format_name",
        "-show_entries", "stream=index,codec_name,codec_type,width,height,r_frame_rate,bit_rate,sample_rate,channels",
        "-print_format", "json"
    ]
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    
    return json.loads(result.stdout)