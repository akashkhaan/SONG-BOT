import os
import time
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = "7434039626:AAG88nBbeX_AfE7KWt72OKyLLZn1GU9pbL0"
OWNER_ID = 8062021892

# 🔗 Your Links
YOUTUBE_LINK = "https://youtube.com/@techtrickindia9?si=QNIhbr4nQbF6RbC8"
SECOND_BOT = "https://t.me/techtricksmsbot"
CONTACT_ADMIN = "https://t.me/TechTrickIndia3"
CHANNEL_LINK = "https://t.me/TechTrickIndia"

# =========================
# 1️⃣ MASS TITLE CHANGE
# =========================
def mass(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        update.message.reply_text("❌ Ye command sirf bot owner use karega.")
        return

    chat_id = update.effective_chat.id
    admins = context.bot.get_chat_administrators(chat_id)

    for admin in admins:
        try:
            context.bot.set_chat_administrator_custom_title(
                chat_id,
                admin.user.id,
                "🔥 KING 🔥"
            )
            time.sleep(0.2)
        except:
            pass

    update.message.reply_text("✅ Sab admins ka title change ho gaya!")

# =========================
# 2️⃣ SONG PLAY + BUTTONS
# =========================
def play_song(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("❌ Example: /bot kesariya")
        return

    query = " ".join(context.args)
    update.message.reply_text("🔎 Song dhoond raha hoon...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'song.%(ext)s',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)
            file_name = ydl.prepare_filename(info['entries'][0])

        # 🔘 Inline Buttons
        keyboard = [
            [InlineKeyboardButton("🔥 Subscribe YouTube", url=YOUTUBE_LINK)],
            [InlineKeyboardButton("🤖 Automatic Message Bot", url=SECOND_BOT)],
            [InlineKeyboardButton("📢 JOIN Channel", url=CHANNEL_LINK)],
            [InlineKeyboardButton("👤 Contact Admin Support", url=CONTACT_ADMIN)],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_audio(
            audio=open(file_name, 'rb'),
            caption=f"🎵 {query}\n\nSupport & Follow Below 👇",
            reply_markup=reply_markup
        )

        os.remove(file_name)

    except:
        update.message.reply_text("❌ Song nahi mila ya error aa gaya.")

# =========================
# MAIN
# =========================
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("mass", mass))
    dp.add_handler(CommandHandler("bot", play_song))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
