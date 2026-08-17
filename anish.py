import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests
import json

# ===== CONFIGURATION =====
BOT_TOKEN = "8779029265:AAFP-zDTsyZzFe2KXcEpivrFZxUJp-NB7TE"
API_URL = "http://markplace.site//api.php"
API_KEY = "demo"

bot = telebot.TeleBot(BOT_TOKEN)

# ===== WELCOME =====
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn = KeyboardButton("📱 Enter Number")
    markup.add(btn)
    bot.reply_to(message, "🔥 Welcome To OFFICIAL_cyber_satyam27 🔥", reply_markup=markup)

# ===== HANDLE NUMBER BUTTON =====
@bot.message_handler(func=lambda msg: msg.text == "📱 Enter Number")
def ask_number(message):
    bot.reply_to(message, "📱 Send Your 10 Digit Number:")

# ===== HANDLE NUMBER INPUT - JSON OUTPUT =====
@bot.message_handler(func=lambda msg: msg.text and msg.text.isdigit() and len(msg.text) == 10)
def search_number(message):
    number = message.text.strip()
    
    msg = bot.reply_to(message, f"⏳ Searching for {number}...")
    
    try:
        params = {
            'key': API_KEY,
            'type': 'number',
            'num': number
        }
        response = requests.get(API_URL, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            bot.delete_message(message.chat.id, msg.message_id)
            
            # DIRECT JSON OUTPUT - RAW API RESPONSE
            json_output = json.dumps(data, indent=2, ensure_ascii=False)
            
            # Check length - agar bahut lamba hai toh split karna padega
            if len(json_output) > 4000:
                # Split into multiple messages
                chunks = [json_output[i:i+4000] for i in range(0, len(json_output), 4000)]
                for chunk in chunks:
                    bot.reply_to(message, f"```json\n{chunk}\n```", parse_mode='Markdown')
            else:
                bot.reply_to(message, f"```json\n{json_output}\n```", parse_mode='Markdown')
                
        else:
            bot.reply_to(message, f"❌ HTTP Error: {response.status_code}")
            
    except requests.exceptions.Timeout:
        bot.reply_to(message, "⏰ Timeout! API not responding.")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, "🌐 Connection Error!")
    except json.JSONDecodeError:
        bot.reply_to(message, "⚠️ Invalid JSON response from API")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# ===== HANDLE INVALID INPUT =====
@bot.message_handler(func=lambda msg: True)
def handle_invalid(message):
    if message.text and message.text.isdigit() and len(message.text) != 10:
        bot.reply_to(message, "⚠️ Send exactly 10 digits!")
    elif message.text and not message.text.isdigit():
        bot.reply_to(message, "⚠️ Only numbers allowed!")

# ===== START BOT =====
print("🔥 OFFICIAL_cyber_satyam27 Bot RUNNING...")
bot.infinity_polling()