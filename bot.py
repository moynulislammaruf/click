import os
import telebot
from telebot import types

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 5988572342  # তোমার Telegram ID
users = set()

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    users.add(message.chat.id)

    text = "👋 স্বাগতম!\n👇 নিচের অপশনগুলো ব্যবহার করুন:"
    markup = types.InlineKeyboardMarkup()

    # Video Button (Temporary)
    markup.add(types.InlineKeyboardButton(
        text="❓ কিভাবে ইনকাম করবেন?",
        url="https://t.me/NoVideoUploadedNow"
    ))

    # Mini App Button with dynamic referral
    referral_link = f"https://t.me/Click_To_Earn_By_Nobab_Bot?start={message.chat.id}"
    markup.add(types.InlineKeyboardButton(
        text="🚀 ইনকাম শুরু করতে এখানে চাপুন",
        url=referral_link
    ))

    # Channel Button
    markup.add(types.InlineKeyboardButton(
        text="📢 চ্যানেলে যুক্ত হই",
        url="https://t.me/Click_To_Earn_By_Nobab_Channel"
    ))

    # New Button: আমার রেফার লিংক
    markup.add(types.InlineKeyboardButton(
        text="📎 আমার রেফার লিংক",
        callback_data="send_referral"
    ))

    bot.send_message(message.chat.id, text, reply_markup=markup)

# Callback handler for "📎 আমার রেফার লিংক"
@bot.callback_query_handler(func=lambda call: call.data == "send_referral")
def send_referral_link(call):
    user_id = call.from_user.id
    referral_link = f"https://t.me/Click_To_Earn_By_Nobab_Bot?start={user_id}"
    text = f"রেফার করে আয় করতে আপনার লিংকটি বন্ধুদের মাঝে ছড়িয়ে দিন।\n\nআপনার রেফার লিংক :- {referral_link}"
    bot.send_message(user_id, text)

# Text Broadcast
@bot.message_handler(commands=['broadcast'])
def broadcast_text(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ এই কমান্ড শুধু Admin ব্যবহার করতে পারবে")
        return

    msg = message.text.replace("/broadcast", "").strip()
    if not msg:
        bot.reply_to(message, "লিখো: /broadcast তোমার মেসেজ")
        return

    sent = 0
    for user_id in users:
        try:
            bot.send_message(user_id, msg)
            sent += 1
        except:
            pass

    bot.reply_to(message, f"✅ {sent} জন ইউজারের কাছে টেক্সট পাঠানো হয়েছে")

# Photo + Caption Broadcast
@bot.message_handler(content_types=['photo'])
def broadcast_photo(message):
    if message.chat.id != ADMIN_ID:
        return

    users.add(message.chat.id)

    photo_id = message.photo[-1].file_id
    caption = message.caption if message.caption else ""

    sent = 0
    for user_id in users:
        try:
            bot.send_photo(user_id, photo_id, caption=caption)
            sent += 1
        except:
            pass

    bot.send_message(message.chat.id, f"✅ {sent} জন ইউজারের কাছে ছবি সহ মেসেজ পাঠানো হয়েছে")

bot.infinity_polling()
