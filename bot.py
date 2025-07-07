import os
import asyncio
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, MenuButtonWebApp
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram.constants import ChatAction

# --- تنظیمات اصلی ---
# توکن ربات شما
BOT_TOKEN = "7446257807:AAGsnNScHj97hKrQ4NRwSmwe5LQrG_SSH40"
# آدرس مینی اپ شما که در دکمه منو قرار می‌گیرد
WEB_APP_URL = "https://abolfazldehghana.github.io/my-telegram-bot/"

# --- تنظیمات گوگل شیت ---
# نام فایل JSON که از گوگل دریافت کردید
GOOGLE_CREDENTIALS_FILE = 'credentials.json'
# نام دقیق شیت گوگلی که می‌خواهید اطلاعات در آن ذخیره شود
GOOGLE_SHEET_NAME = 'ForexKillerUsers' # مثال: 'Users' - این شیت باید از قبل ساخته شده باشد

# تعریف دسترسی‌های مورد نیاز
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# --- تابع اتصال و ذخیره در گوگل شیت ---
def update_google_sheet(user_id, username, first_name, last_name, campaign_source):
    """اطلاعات کاربر را در یک ردیف جدید در گوگل شیت وارد می‌کند"""
    try:
        # احراز هویت و اتصال به گوگل شیت
        creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_FILE, SCOPE)
        client = gspread.authorize(creds)
        sheet = client.open(GOOGLE_SHEET_NAME).sheet1 # اتصال به اولین شیت (برگه)

        # بررسی اینکه آیا هدرها قبلاً نوشته شده‌اند یا نه
        if not sheet.get_all_values() or sheet.row_values(1) != ['User ID', 'Username', 'First Name', 'Last Name', 'Start Date', 'Campaign Source']:
             sheet.append_row(['User ID', 'Username', 'First Name', 'Last Name', 'Start Date', 'Campaign Source'])


        # آماده‌سازی ردیف جدید برای افزودن
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row_to_add = [
            str(user_id),
            username or 'N/A',
            first_name or 'N/A',
            last_name or 'N/A',
            current_time,
            campaign_source
        ]

        # افزودن ردیف جدید به شیت
        sheet.append_row(row_to_add)
        print(f"کاربر جدید با موفقیت در گوگل شیت ذخیره شد: {username}")
        return True
    except FileNotFoundError:
        print(f"خطا: فایل '{GOOGLE_CREDENTIALS_FILE}' پیدا نشد. لطفاً آن را در کنار فایل ربات قرار دهید.")
        return False
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"خطا: گوگل شیت با نام '{GOOGLE_SHEET_NAME}' پیدا نشد. از صحت نام و دسترسی ربات اطمینان حاصل کنید.")
        return False
    except Exception as e:
        print(f"یک خطای پیش‌بینی نشده در اتصال به گوگل شیت رخ داد: {e}")
        return False

# --- توابع اصلی ربات ---

async def start(update: Update, context):
    """
    پیام خوشامدگویی را ارسال، دکمه منو را تنظیم و اطلاعات کاربر را در گوگل شیت ذخیره می‌کند
    """
    user = update.effective_user
    
    # --- مدیریت لینک‌های کمپین ---
    # لینک‌های شما به این شکل خواهند بود: t.me/YourBot?start=campaign1
    campaign_source = 'Direct' # مقدار پیش‌فرض اگر کاربر مستقیم وارد شود
    if context.args:
        campaign_source = context.args[0] # نام کمپین از لینک استخراج می‌شود

    # ذخیره اطلاعات در گوگل شیت
    update_google_sheet(user.id, user.username, user.first_name, user.last_name, campaign_source)

    # --- تنظیم دکمه منوی اصلی برای باز کردن مینی‌اپ ---
    await context.bot.set_chat_menu_button(
        chat_id=update.effective_chat.id,
        menu_button=MenuButtonWebApp(text="🚀 ورود به برنامه", web_app=WebAppInfo(url=WEB_APP_URL))
    )

    # --- ارسال پیام‌های خوشامدگویی ---
    await update.message.reply_text(
        "به ربات کسب درآمد دلاری فارکس کیلر خوش امدید"
    )

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(3)

    await update.message.reply_text(
        "در اینجا قراره باهم از طریق شیوه ای کاملا شناخته شده خیلی "
        "راحت به دور از هرسختی و ریسک درآمد دلاری داشته باشیم"
    )

    keyboard = [[InlineKeyboardButton("✅ شروع", callback_data='start_button_pressed')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "برای شروع روی دکمه زیر بزن:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context):
    """کلیک روی دکمه‌های شیشه‌ای را مدیریت می‌کند"""
    query = update.callback_query
    await query.answer()

    if query.data == 'start_button_pressed':
        await query.edit_message_text(
            text="عالیه! برای ورود به برنامه و شروع کسب درآمد، از دکمه منو 🚀 در پایین صفحه استفاده کن."
        )

def main():
    """ربات را راه‌اندازی و اجرا می‌کند"""
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()
