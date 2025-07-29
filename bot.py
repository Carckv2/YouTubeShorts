import traceback
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from shorts_maker import generate_shorts

BOT_TOKEN = "7797157259:AAHf5OPT_peyWLQV-4RsI-EPMsFUoF3Iqng"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome! Send /shorts <YouTube URL> to create a Shorts video with title and description captions."
    )

async def shorts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❌ Please provide a YouTube link.\nExample:\n/shorts https://www.youtube.com/watch?v=..."
        )
        return

    url = context.args[0]
    await update.message.reply_text("⏳ Processing your video. Please wait...")

    try:
        shorts_path = generate_shorts(url)
        with open(shorts_path, "rb") as video_file:
            await update.message.reply_video(video=video_file, caption="✅ Here is your Shorts video!")
    except Exception as e:
        logging.error(f"Error processing video: {e}")
        logging.error(traceback.format_exc())
        await update.message.reply_text(f"❌ Failed to generate Shorts.\nError:\n{e}\nPlease try again later.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("shorts", shorts_command))
    print("Bot started. Listening for commands...")
    app.run_polling()
