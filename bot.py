# for installing the library: pip install python-telegram-bot
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler

# ====================================================================
# توکن ربات شما در اینجا قرار گرفته است
# ====================================================================
BOT_TOKEN = "7048334360:AAEkI9RiF-vUYvUq6Sg92Q9oiE5OjFAaHok"


# این تابع زمانی اجرا می‌شود که کاربر دستور /start را ارسال کند
async def start(update: Update, context):
    """Sends a message with three inline buttons."""
    # ساخت دکمه‌های شیشه‌ای (زیر پیام)
    keyboard = [
        [InlineKeyboardButton("گزینه اول 🥇", callback_data='option_1')],
        [InlineKeyboardButton("گزینه دوم 🥈", callback_data='option_2')],
        [InlineKeyboardButton("راهنما ❓", callback_data='help')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # ارسال پیام خوشامدگویی به همراه دکمه‌ها
    await update.message.reply_text(
        "سلام! به ربات من خوش آمدید. لطفا یک گزینه را انتخاب کنید:",
        reply_markup=reply_markup
    )

# این تابع زمانی اجرا می‌شود که یکی از دکمه‌های شیشه‌ای فشار داده شود
async def button_handler(update: Update, context):
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()

    # بر اساس دکمه فشرده شده، یک پاسخ متفاوت ارسال می‌کنیم
    if query.data == 'option_1':
        await query.edit_message_text(text="شما گزینه اول را انتخاب کردید.")
    elif query.data == 'option_2':
        await query.edit_message_text(text="شما گزینه دوم را انتخاب کردید.")
    elif query.data == 'help':
        await query.edit_message_text(text="این یک ربات نمونه است. برای شروع مجدد /start را بزنید.")

# این تابع به هر پیام متنی که کامند نباشد، پاسخ می‌دهد
async def echo(update: Update, context):
    """Echo the user message."""
    await update.message.reply_text(f"شما نوشتید: {update.message.text}")


def main():
    """Start the bot."""
    # ساخت اپلیکیشن ربات
    application = Application.builder().token(BOT_TOKEN).build()

    # تعریف دستورات و کنترل‌کننده‌ها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # شروع به کار ربات
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()