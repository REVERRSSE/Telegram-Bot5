import random
import telebot

# Initialize the bot with your token
bot_token = "6208420778:AAE43W9yrSbv5KVnLzADnmXY6oxqGupNGJ8"
bot = telebot.TeleBot(bot_token)


# Function to generate a password
def generate_password(length, type):
    numbers = "0123456789"
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    special_chars = "!@#$%^&*()_+-={}[]:;',.<>?|~`"

    if type == "random":
        all_chars = numbers + letters + special_chars
    elif type == "letters and numbers only":
        all_chars = numbers + letters
    else:  # Default to a mix of letters and numbers
        all_chars = numbers + letters

    return ''.join(random.choice(all_chars) for _ in range(length))


# Handler for /start command
@bot.message_handler(commands=['start'])
def start(message):
    msg = ("Please reply with the following details:\n"
           "1. Account name:\n"
           "2. User name:\n"
           "3. Password length (choose between 6-12):\n"
           "4. Type of password:\n"
           " - random\n"
           " - letters and numbers only\n"
           " - enter your own password")
    bot.send_message(message.chat.id, msg)


# Handler for regular messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Parse the user's message for required details
    details = message.text.split('\n')
    if len(details) >= 4:
        account_name = details[0]
        user_name = details[1]
        try:
            length = int(details[2])
            length = max(6, min(length, 12))  # Ensure length is between 6 and 12
        except ValueError:
            bot.send_message(message.chat.id, "Invalid length. Please enter a number between 6 and 12.")
            return

        type = details[3]
        if type not in ["random", "letters and numbers only"]:
            type = "random"  # Default to random if an invalid type is provided

        # Generate password
        password = generate_password(length, type)
        bot.send_message(message.chat.id, f"Generated password for {account_name} ({user_name}): {password}")
    else:
        bot.send_message(message.chat.id, "Please provide all required details.")


# Start polling
bot.polling(none_stop=True)
    