import os
import ffmpeg
from pytube import YouTube
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_youtube_video(url: str):
    yt = YouTube(url)
    title = yt.title.replace(" ", "_").replace("/", "_")
    description = yt.description.strip().replace("\n", " ")
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    filepath = os.path.join(OUTPUT_DIR, f"{title}.mp4")
    if not os.path.exists(filepath):
        stream.download(output_path=OUTPUT_DIR, filename=f"{title}.mp4")
    return filepath, title, description

def create_caption_clips(title: str, description: str, video_width: int, video_height: int):
    title_clip = (TextClip(title, fontsize=60, font='Arial-Bold',
                           color='white', stroke_color='black', stroke_width=3,
                           size=(video_width - 40, None), method='caption')
                  .set_position(('center', 'top'))
                  .set_duration(7))

    description_clip = (TextClip(description[:300] + ("..." if len(description) > 300 else ""), fontsize=40, font='Arial',
                                color='white', stroke_color='black', stroke_width=2,
                                size=(video_width - 40, None), method='caption')
                        .set_position(('center', 'bottom'))
                        .set_start(7)
                        .set_duration(10))

    return [title_clip, description_clip]

def burn_captions(video_path: str, title: str, description: str):
    video = VideoFileClip(video_path)
    captions = create_caption_clips(title, description, video.w, video.h)
    final = CompositeVideoClip([video, *captions])
    out_path = os.path.join(OUTPUT_DIR, f"{title}_captioned.mp4")
    final.write_videofile(out_path, codec='libx264', audio_codec='aac', fps=video.fps)
    return out_path

def convert_to_vertical(input_path: str, title: str):
    output_path = os.path.join(OUTPUT_DIR, f"{title}_shorts.mp4")
    probe = ffmpeg.probe(input_path)
    stream = next(s for s in probe["streams"] if s["codec_type"] == "video")
    width, height = int(stream["width"]), int(stream["height"])

    if height > width:
        os.rename(input_path, output_path)
        return output_path

    new_width = int(height * 9 / 16)
    x_offset = (width - new_width) // 2

    (
        ffmpeg
        .input(input_path)
        .filter("crop", new_width, height, x_offset, 0)
        .output(output_path, vcodec="libx264", acodec="aac")
        .overwrite_output()
        .run()
    )
    return output_path

def generate_shorts(url: str):
    video_path, title, description = download_youtube_video(url)
    captioned_path = burn_captions(video_path, title, description)
    shorts_path = convert_to_vertical(captioned_path, title)
    return shorts_path
