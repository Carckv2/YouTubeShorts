
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from core.downloader import download_video
from core.transcriber import transcribe_audio
from core.clipper import get_mrbeast_clips
from core.generator import generate_title_description
import os

def start(update: Update, ctx: CallbackContext):
    update.message.reply_text("Send /short <YouTube Link> to generate MrBeast-style Shorts.")

def short(update: Update, ctx: CallbackContext):
    if not ctx.args:
        update.message.reply_text("Please provide a YouTube link.")
        return
    url = ctx.args[0]
    update.message.reply_text("Downloading and processing video...")

    video_path = download_video(url)
    transcript = transcribe_audio(video_path)
    clips = get_mrbeast_clips(video_path, transcript)

    for clip in clips:
        title, desc = generate_title_description(clip["transcript"])
        with open(clip["path"], "rb") as f:
            update.message.reply_video(video=f, caption=f"{title}

{desc}")

updater = Updater("7797157259:AAHf5OPT_peyWLQV-4RsI-EPMsFUoF3Iqng")
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("short", short))
updater.start_polling()
