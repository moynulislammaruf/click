import os
import telebot
from telebot import types

# Bot Token will be taken from Environment Variable for security
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN environment variable not set. Please set your Bot Token in hosting platform.")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    text = "👋 স্বাগতম!\n👇 নিচের অপশনগুলো ব্যবহার করুন:"

    markup = types.InlineKeyboardMarkup()

    # Video Button (Temporary)
    markup.add(types.InlineKeyboardButton(
        text="❓ কিভাবে ইনকাম করবেন?",
        url="https://t.me/NoVideoUploadedNow"
    ))

    # Mini App Button
    markup.add(types.InlineKeyboardButton(
        text="🚀 ইনকাম শুরু করতে এখানে চাপুন",
        url="https://t.me/Click_To_Earn_By_Nobab_Bot?startapp=5988572342"
    ))

    # Channel Button (placeholder, change later)
    markup.add(types.InlineKeyboardButton(
        text="📢 চ্যানেলে যুক্ত হই",
        url="https://t.me/YourChannelLink"
    ))

    bot.send_message(message.chat.id, text, reply_markup=markup)

bot.infinity_polling()
