import os
import logging
import asyncio
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from sandbox import execute_plot_code, check_code_safety
from utils import extract_code, format_error_message, get_help_message, get_welcome_message

# Configure logging
import logging.config
import os.path

if os.path.exists('logging.conf'):
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    logging.config.fileConfig('logging.conf')
else:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

logger = logging.getLogger(__name__)

def setup_font():
    """Configure matplotlib to use Times New Roman font (with Liberation Serif fallback)"""
    try:
        # Set font preferences with fallback chain
        plt.rcParams['font.family'] = 'serif'
        plt.rcParams['font.serif'] = ['Times New Roman', 'Liberation Serif', 'DejaVu Serif', 'serif']
        
        # Test if any serif font is available
        fig, ax = plt.subplots(figsize=(1, 1))
        ax.text(0.5, 0.5, 'Test', fontfamily='serif')
        plt.close(fig)
        
        logger.info("Font configuration completed successfully")
    except Exception as e:
        logger.warning(f"Could not configure fonts: {e}")
        # Fallback to matplotlib defaults
        plt.rcParams['font.family'] = 'sans-serif'

# Execute the plotting code safely and return the generated images
async def run_plot_code(code):
    # First check if the code is safe to execute
    is_safe, safety_error = check_code_safety(code)
    if not is_safe:
        error_type, formatted_error = format_error_message(safety_error)
        return [], formatted_error

    # Execute the code in the sandbox
    plot_files, output, error = execute_plot_code(code)
    
    if error:
        logger.error(error)
        error_type, formatted_error = format_error_message(error)
        return [], formatted_error
    
    if output:
        logger.info(f"Code execution output: {output}")
    
    return plot_files, None

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_welcome_message())

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_help_message())

async def process_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    code = extract_code(message_text)
    
    if not code:
        await update.message.reply_text(
            "I couldn't find any Python plotting code in your message. "
            "Please send code enclosed in triple backticks (```). "
            "Type /help for examples."
        )
        return
    
    # Send a processing message
    processing_message = await update.message.reply_text("Processing your plotting code...")
    
    try:
        # Execute the code and get the plot files
        plot_files, error = await run_plot_code(code)
        
        if error:
            await update.message.reply_text(f"Error: {error}")
            return
        
        if not plot_files:
            await update.message.reply_text(
                "No plots were generated. Make sure your code creates plots and includes plt.show()."
            )
            return
        
        # Send each plot as a photo
        for plot_file in plot_files:
            with open(plot_file, 'rb') as f:
                await update.message.reply_photo(photo=f)
        
        # Cleanup temporary files
        for plot_file in plot_files:
            try:
                os.remove(plot_file)
            except Exception as e:
                logger.error(f"Error removing temporary file {plot_file}: {e}")
    
    except Exception as e:
        await update.message.reply_text(f"An unexpected error occurred: {str(e)}")
        logger.error(f"Unexpected error in process_code: {str(e)}")
    
    finally:
        # Always try to delete the processing message
        try:
            await processing_message.delete()
        except Exception:
            pass

def main():
    # Setup font configuration
    setup_font()
    
    # Get the token from environment variable
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("No TELEGRAM_BOT_TOKEN environment variable found")
        return
    
    # Create the Application
    application = Application.builder().token(token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_code))
    
    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()