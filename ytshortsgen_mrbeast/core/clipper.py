
from moviepy.editor import VideoFileClip
import re

def get_mrbeast_clips(video_path, transcript):
    keywords = ["won", "challenge", "crazy", "insane", "surprise", "money", "dollar", "countdown"]
    clips = []
    for i in range(10):  # Top 10 clips for example
        start = i * 60
        end = start + 35
        clip = VideoFileClip(video_path).subclip(start, end)
        out_path = f"data/clip_{i}.mp4"
        clip.write_videofile(out_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)
        clip.close()
        segment = " ".join(transcript.split()[i*50:(i+1)*60])
        if any(re.search(k, segment, re.IGNORECASE) for k in keywords):
            clips.append({"path": out_path, "transcript": segment})
    return clips
