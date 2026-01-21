import os
import telebot
from telebot import types

TOKEN = os.getenv("TOKEN")  # Hosting এ Environment variable হিসেবে বসাতে হবে
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 5988572342  # তোমার Telegram ID
users = set()
referrals = {}  # key: new_user_id, value: referrer_id

# -----------------------------
# Start Command
# -----------------------------
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    users.add(user_id)

    # Check if user came with referral
    try:
        start_param = message.text.split()[1]
        referrer_id = int(start_param)
        referrals[user_id] = referrer_id
    except:
        referrer_id = user_id  # কেউ সরাসরি এসেছে, নিজের ID use

    # Buttons
    markup = types.InlineKeyboardMarkup(row_width=1)

    # 1️⃣ Video placeholder
    video_btn = types.InlineKeyboardButton(
        text="🎬 কিভাবে ইনকাম করবেন?",
        url="https://t.me/NoVideoUploadedNow"
    )

    # 2️⃣ Mini App Button with startapp parameter
    mini_app_link = f"https://t.me/Click_To_Earn_By_Nobab_Bot?startapp={referrer_id}"
    earn_btn = types.InlineKeyboardButton(
        text="🚀 ইনকাম শুরু করুন",
        url=mini_app_link
    )

    # 3️⃣ Channel Button
    channel_btn = types.InlineKeyboardButton(
        text="📢 চ্যানেলে যুক্ত হই",
        url="https://t.me/Click_To_Earn_By_Nobab_Channel"
    )

    # 4️⃣ Referral Button
    referral_btn = types.InlineKeyboardButton(
        text="📎 আমার রেফার লিংক",
        callback_data="send_referral"
    )

    markup.add(video_btn, earn_btn, channel_btn, referral_btn)

    welcome_text = "👋 স্বাগতম!\n\nনিচের বাটনগুলো ব্যবহার করে শুরু করুন:"
    bot.send_message(user_id, welcome_text, reply_markup=markup)

# -----------------------------
# Callback handler for referral link
# -----------------------------
@bot.callback_query_handler(func=lambda call: call.data == "send_referral")
def send_referral_link(call):
    user_id = call.from_user.id
    referral_link = f"https://t.me/Click_To_Earn_By_Nobab_Bot?start={user_id}"
    text = f"💰 রেফার করে আয় করতে আপনার লিংকটি বন্ধুদের মাঝে ছড়িয়ে দিন।\n\n🔗 আপনার রেফার লিংক: {referral_link}"
    bot.send_message(user_id, text)

# -----------------------------
# Text Broadcast (Admin only)
# -----------------------------
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

# -----------------------------
# Photo + Caption Broadcast (Admin only)
# -----------------------------
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

# -----------------------------
# Start Polling
# -----------------------------
bot.infinity_polling()
