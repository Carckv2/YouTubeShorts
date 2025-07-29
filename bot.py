import traceback
import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from shorts_maker import generate_shorts

BOT_TOKEN = "7797157259:AAHf5OPT_peyWLQV-4RsI-EPMsFUoF3Iqng"  # Keep this secure!

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def is_valid_youtube_url(url: str) -> bool:
    return "youtube.com/watch" in url or "youtu.be/" in url

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome! Send /shorts <YouTube URL> to create a Shorts video with title and description captions.\n"
        "Use /help for more info."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📌 *YouTube Shorts Generator Bot*\n\n"
        "Use /shorts followed by one or more YouTube link(s) to get Shorts video(s) with captions.\n\n"
        "Example:\n"
        "/shorts https://youtu.be/xyz123 https://www.youtube.com/watch?v=abc456\n\n"
        "The video(s) will be processed and sent back as vertical Shorts with title and description captions."
    )
    await update.message.reply_markdown(help_text)

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Pong! Bot is alive and ready.")

async def shorts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❌ Please provide at least one YouTube link.\nExample:\n/shorts https://www.youtube.com/watch?v=..."
        )
        return

    await update.message.reply_text("⏳ Processing your video(s). Please wait...")

    for url in context.args:
        if not is_valid_youtube_url(url):
            await update.message.reply_text(f"❌ Invalid YouTube URL:\n{url}")
            continue

        try:
            shorts_path = generate_shorts(url)
            file_size_mb = os.path.getsize(shorts_path) / (1024 * 1024)
            if file_size_mb > 50:
                await update.message.reply_text(
                    f"⚠️ Video too large to send ({file_size_mb:.2f} MB). Skipping:\n{url}"
                )
                continue

            with open(shorts_path, "rb") as video_file:
                await update.message.reply_video(video=video_file, caption=f"✅ Shorts video for:\n{url}")
        except Exception as e:
            logging.error(f"Error processing video {url}: {e}")
            logging.error(traceback.format_exc())
            await update.message.reply_text(f"❌ Failed to generate Shorts for:\n{url}\nError:\n{e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("shorts", shorts_command))

    print("Bot started. Listening for commands...")
    app.run_polling()
