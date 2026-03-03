import logging
import os
import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import TELEGRAM_BOT_TOKEN, LOG_FILE
import database
from handlers.commands import (
    start_command, help_command, learn_command, quiz_command, 
    debug_command, run_command, progress_command, weakareas_command, 
    interview_command, handle_message
)
from scheduler import DevCoreScheduler

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    format=\'%(asctime)s - %(name)s - %(levelname)s - %(message)s\',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    \"\"\"Log the error and send a telegram message to notify the developer.\"\"\"
    logger.error(f\"Exception while handling an update: {context.error}\")
    
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            \"An unexpected error occurred. My engineers have been notified. Please try again later.\"
        )

def main():
    \"\"\"Start the bot.\"\"\"
    # Ensure environment variables are set
    if not TELEGRAM_BOT_TOKEN:
        print(\"ERROR: TELEGRAM_BOT_TOKEN environment variable not set.\")
        sys.exit(1)
        
    # Initialize Database
    database.init_db()
    
    # Build the Application
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add Command Handlers
    application.add_handler(CommandHandler(\"start\", start_command))
    application.add_handler(CommandHandler(\"help\", help_command))
    application.add_handler(CommandHandler(\"learn\", learn_command))
    application.add_handler(CommandHandler(\"quiz\", quiz_command))
    application.add_handler(CommandHandler(\"debug\", debug_command))
    application.add_handler(CommandHandler(\"run\", run_command))
    application.add_handler(CommandHandler(\"progress\", progress_command))
    application.add_handler(CommandHandler(\"weakareas\", weakareas_command))
    application.add_handler(CommandHandler(\"interview\", interview_command))
    
    # Add Message Handler for non-command messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add Error Handler
    application.add_error_handler(error_handler)
    
    # Initialize Scheduler
    bot_instance = application.bot
    scheduler = DevCoreScheduler(bot_instance)
    scheduler.start()
    
    # Run the bot
    print(\"DevCore Bot is starting...\")
    application.run_polling()

if __name__ == \'__main__\':
    main()
