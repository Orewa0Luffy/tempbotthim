import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler
from config import BOT_TOKEN
from utils.generator import generate_thumbnail

user_data = {}

logging.basicConfig(level=logging.INFO)

TEMPLATE_CHOICES = {
    "Blue Lock": "blue_lock",
    "Naruto Shippuden 1": "naruto1",
    "Naruto Shippuden 2": "naruto2"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎨 Create Thumbnail", callback_data="start_create")],
        [InlineKeyboardButton("📢 Updates", url="https://t.me/Animes_Union")],
        [InlineKeyboardButton("❓ Help", callback_data="help")]
    ]
    await update.message.reply_text(
        "👋 Welcome to Anime Thumbnail Bot!\nUse /create <title> to start.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /create <anime title> to make a thumbnail.")

async def create(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /create <Anime Title>")
        return
    user_id = update.message.from_user.id
    user_data[user_id] = {"title": " ".join(context.args)}

    # Send template options
    buttons = [
        [InlineKeyboardButton(name, callback_data=f"template_{key}")]
        for name, key in TEMPLATE_CHOICES.items()
    ]
    await update.message.reply_text("Choose a template:", reply_markup=InlineKeyboardMarkup(buttons))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "start_create":
        await context.bot.send_message(chat_id=user_id, text="Send /create <Anime Title> to begin.")
        return

    if query.data == "help":
        await context.bot.send_message(chat_id=user_id, text="Send an anime title and pick a template.")
        return

    if query.data.startswith("template_"):
        template = query.data.replace("template_", "")
        user_data[user_id]["template"] = template
        await context.bot.send_message(chat_id=user_id, text="Now send the anime image.")

async def image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in user_data or "template" not in user_data[user_id]:
        return await update.message.reply_text("Please use /create first.")

    photo = await update.message.photo[-1].get_file()
    file_path = f"downloads/{user_id}.jpg"
    os.makedirs("downloads", exist_ok=True)
    await photo.download_to_drive(file_path)
    user_data[user_id]["image"] = file_path
    await update.message.reply_text("Now send the synopsis/description.")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in user_data and "image" in user_data[user_id]:
        user_data[user_id]["synopsis"] = update.message.text
        title = user_data[user_id]["title"]
        template = user_data[user_id]["template"]
        synopsis = user_data[user_id]["synopsis"]
        image_path = user_data[user_id]["image"]

        await update.message.reply_text("Creating thumbnail...")
        output = generate_thumbnail(template, title, synopsis, image_path)
        await update.message.reply_photo(photo=open(output, 'rb'))

        # Cleanup
        del user_data[user_id]

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("create", create))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, image_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("Bot started...")
    app.run_polling()
