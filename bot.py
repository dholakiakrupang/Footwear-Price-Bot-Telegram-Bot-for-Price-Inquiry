import logging
import sys
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import config
import db

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

async def start(update, context):
    """Greets the user and provides instructions."""
    username = update.effective_user.username
    if username not in config.APPROVED_USERS:
        await update.message.reply_text("Sorry, you're not authorized to use this bot.")
        return

    await update.message.reply_text(
        "Hi! I'm a Giriraj Footwear bot that provides prices of different footwear. "
        "Please enter a 3-digit number to get its corresponding Price. "
        "Use /help to see available commands."
    )

async def help_command(update, context):
    """Sends a list of available commands."""
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot and get instructions\n"
        "/help - Show this help message\n"
        "/add_output <input> <normal_output> <special_output1> <special_output2> - Add a new output for a specific input\n"
        "/delete_output <input> - Delete the output for a specific input\n"
        "/update_output <input> <normal_output> <special_output1> <special_output2> - Update the output for a specific input\n"
    )

async def handle_message(update, context):
    """Processes user input."""
    text = update.message.text

    # Check if user is approved
    username = update.effective_user.username
    if username not in config.APPROVED_USERS:
        await update.message.reply_text("Sorry, you're not authorized to use this bot.")
        return

    # Validate input (3 digits only)
    if not text.isdigit() or len(text) != 3:
        await update.message.reply_text("Please enter a valid 3-digit number.")
        return

    # Get output mapping from the database
    output = db.get_output_mapping(text)
    if output is None:
        await update.message.reply_text("No output defined for this input.")
        return

    normal_output, special_output1, special_output2 = output

    # Get user type (normal or special)
    user_type = db.get_user_type(username) or 'normal'

    # Retrieve output based on user type
    if user_type == 'special':
        await update.message.reply_text(f"Selling Price: {special_output1}\nCost Price: {special_output2}")
    else:
        await update.message.reply_text(normal_output)

async def add_output(update, context):
    """Adds a new output for a specific input."""
    args = context.args
    if len(args) != 4:
        await update.message.reply_text("Invalid number of arguments. Usage: /add_output input normal_output special_output1 special_output2")
        return

    input_digit, normal_output, special_output1, special_output2 = args

    # Check if the input is a 3-digit number
    if not input_digit.isdigit() or len(input_digit) != 3:
        await update.message.reply_text("Please enter a valid 3-digit input number.")
        return

    db.add_output_mapping(input_digit, normal_output, special_output1, special_output2)
    await update.message.reply_text("Output added successfully!")

async def delete_output(update, context):
    """Deletes the output for a specific input."""
    args = context.args
    if len(args) != 1:
        await update.message.reply_text("Invalid number of arguments. Usage: /delete_output input")
        return

    input_digit = args[0]

    # Check if the input is a 3-digit number
    if     not input_digit.isdigit() or len(input_digit) != 3:
        await update.message.reply_text("Please enter a valid 3-digit input number.")
        return

    db.delete_output_mapping(input_digit)
    await update.message.reply_text("Output deleted successfully!")

async def update_output(update, context):
    """Updates the output for a specific input."""
    args = context.args
    if len(args) != 4:
        await update.message.reply_text("Invalid number of arguments. Usage: /update_output input normal_output special_output1 special_output2")
        return

    input_digit, normal_output, special_output1, special_output2 = args

    # Check if the input is a 3-digit number
    if not input_digit.isdigit() or len(input_digit) != 3:
        await update.message.reply_text("Please enter a valid 3-digit input number.")
        return

    db.update_output_mapping(input_digit, normal_output, special_output1, special_output2)
    await update.message.reply_text("Output updated successfully!")

def main():
    """Starts the Telegram bot."""
    db.init_db()  # Initialize the database

    api_token = config.API_TOKEN
    if not api_token:
        print("No TELEGRAM_API_TOKEN found in environment variables. Please set the token and try again.")
        sys.exit(1)

    application = Application.builder().token(api_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CommandHandler("add_output", add_output))
    application.add_handler(CommandHandler("delete_output", delete_output))
    application.add_handler(CommandHandler("update_output", update_output))

    application.run_polling()

if __name__ == '__main__':
    main()
