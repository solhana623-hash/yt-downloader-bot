import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# BotFather የሰጠህን ቶከን እዚህ ጋር በዝርዝር አስገባ
TOKEN = '8275184653:AAEyvmptnOq2274Wmd1N3SChlPqRVowF0kQ'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("እንኳን መጡ! የዩቱብ ሊንክ ይላኩልኝና በፈለጉት ጥራት አውርድልዎታለሁ።")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "youtube.com" in url or "youtu.be" in url:
        await update.message.reply_text("ቪዲዮውን በማዘጋጀት ላይ ነኝ... እባክዎ በትዕግስት ይጠብቁ።")
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.mp4',
            'max_filesize': 50 * 1024 * 1024  # ለጊዜው እስከ 50MB ብቻ
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            await update.message.reply_video(video=open('video.mp4', 'rb'))
            os.remove('video.mp4')
        except Exception as e:
            await update.message.reply_text(f"ስህተት አጋጥሟል፦ {str(e)}")
    else:
        await update.message.reply_text("እባክዎ ትክክለኛ የዩቱብ ሊንክ ይላኩ።")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    app.run_polling()

if __name__ == '__main__':
    main()
