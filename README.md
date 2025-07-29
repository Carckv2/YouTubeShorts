# YouTube Shorts Generator Telegram Bot

## Overview

This Telegram bot downloads a YouTube video from a provided link, burns the **video's title and description as captions** into the video, crops it to a **vertical 9:16 format** for YouTube Shorts, and sends back the processed Shorts video.

**No audio transcription** is done, since the audio is assumed to be already present in the video (e.g. MrBeast videos).

---

## Requirements

- Python 3.11.13
- `ffmpeg` installed on your system and in your PATH

---

## Setup

1. Clone or download this repository.

2. Install dependencies:

```bash
pip install -r requirements.txt
