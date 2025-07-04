import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram.constants import ChatAction

# توکن ربات شما
BOT_TOKEN = "7048334360:AAEkI9RiF-vUYvUq6Sg92Q9oiE5OjFAaHok"

# نام کاربری کانال شما آپدیت شد
YOUR_CHANNEL_USERNAME = "forexkiller_vip"


# این تابع برای دستور /start اجرا می‌شود
async def start(update: Update, context):
    user_name = update.effective_user.first_name

    # مرحله ۱: ارسال پیام خوشامدگویی
    await update.message.reply_text(
        f"سلام {user_name} عزیز، به ربات فارکس کیلر خوش اومدی 🚀"
    )

    # مرحله ۲: نمایش حالت تایپینگ و ارسال پیام بعدی
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(1.5)  # تاخیر برای طبیعی‌تر شدن
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="در این ربات میتونی کاملا رایگان عضو بهترین کانال‌های سیگنال بشی. فقط کافیه چند مرحله ابتدایی رو با این ربات انجام بدی."
    )

    # مرحله ۳: دکمه عضویت در کانال
    keyboard = [
        [InlineKeyboardButton("عضویت در کانال تلگرام", url=f"https://t.me/{YOUR_CHANNEL_USERNAME}")],
        [InlineKeyboardButton("✅ عضو شدم و ادامه", callback_data="joined_channel")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="عضویت و تمامی خدمات این ربات رایگانه! فقط کافیه برای حمایت از ما عضو کانال زیر بشی و بعد از عضویت، روی دکمه 'عضو شدم' کلیک کنی.",
        reply_markup=reply_markup
    )


# این تابع برای مدیریت دکمه‌های شیشه‌ای اجرا می‌شود
async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()

    # مرحله ۴: پس از کلیک روی "عضو شدم"
    if query.data == "joined_channel":
        trade_keyboard = [
            [InlineKeyboardButton("جفت ارزهای اصلی  Forex", callback_data="trade_majors")],
            [InlineKeyboardButton("طلا و فلزات گرانبها 🪙", callback_data="trade_metals")],
            [InlineKeyboardButton("شاخص‌های جهانی 📈", callback_data="trade_indices")],
            [InlineKeyboardButton("نفت و انرژی 🛢️", callback_data="trade_energy")],
        ]
        reply_markup = InlineKeyboardMarkup(trade_keyboard)
        await query.edit_message_text(
            text="عالی! حالا انتخاب کن که بیشتر به ترید روی چه نمادهایی علاقه داری؟",
            reply_markup=reply_markup
        )
    
    # اینجا می‌توانید برای هر دکمه یک منطق جداگانه بنویسید
    elif query.data == "trade_majors":
        await query.edit_message_text(text="شما 'جفت ارزهای اصلی' را انتخاب کردید. مرحله بعدی به زودی اضافه خواهد شد.")
    
    elif query.data == "trade_metals":
        await query.edit_message_text(text="شما 'طلا و فلزات' را انتخاب کردید. مرحله بعدی به زودی اضافه خواهد شد.")
        
    elif query.data == "trade_indices":
        await query.edit_message_text(text="شما 'شاخص‌های جهانی' را انتخاب کردید. مرحله بعدی به زودی اضافه خواهد شد.")

    elif query.data == "trade_energy":
        await query.edit_message_text(text="شما 'نفت و انرژی' را انتخاب کردید. مرحله بعدی به زودی اضافه خواهد شد.")


def main():
    """Start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()