import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, MenuButtonWebApp
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# --- تنظیمات ---
BOT_TOKEN = "7048334360:AAEkI9RiF-vUYvUq6Sg92Q9oiE5OjFAaHok"
# آدرس مینی اپ شما که از گیت‌هاب گرفتید
WEB_APP_URL = "https://abolfazldehghana.github.io/my-telegram-bot/"


# --- توابع ربات ---

async def start(update: Update, context):
    """
    این تابع دکمه منوی اصلی را تنظیم می‌کند و پیام خوشامدگویی می‌فرستد
    """
    await context.bot.set_chat_menu_button(
        chat_id=update.effective_chat.id,
        menu_button=MenuButtonWebApp(text="🚀 ورود به بازی", web_app=WebAppInfo(url=WEB_APP_URL))
    )
    await update.message.reply_text(
        "سلام! به ربات فارکس کیلر خوش اومدی 🚀\n\n"
        "برای شروع سفر مالی خودت، از دکمه منوی پایین (یا علامت 📎) استفاده کن و روی 'ورود به بازی' کلیک کن!"
    )

def main():
    """Start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    print("Bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()