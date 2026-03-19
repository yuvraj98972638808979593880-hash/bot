import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

TOKEN = "8321891559:AAFeqTvIGrfGVXNWziOo38qy2g7ujfWD4rc"
PASSWORD = "HARSHITHACKERH"

users = {}

# Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users[update.effective_user.id] = False
    await update.message.reply_text("🔐 Enter Password:")

# Password check
async def check_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not users.get(user_id):
        if update.message.text == PASSWORD:
            users[user_id] = True
            await update.message.reply_text("✅ Access Granted!\n\nUse /predict")
        else:
            await update.message.reply_text("❌ Wrong Password")
        return

# Generate prediction
def generate():
    size = random.choice(["Big", "Small"])

    if size == "Big":
        number = random.randint(5, 9)
    else:
        number = random.randint(0, 4)

    if number % 2 == 0:
        color = "🔴 Red"
    else:
        color = "🟢 Green"

    return f"""🔥 HARSHIT_BHAI_HACKZ 🔥
━━━━━━━━━━━━━━
⏱ 1 MINUTE WINGO PREDICTION
━━━━━━━━━━━━━━

🎯 Result:
Color: {color}
Size: {size}
Number: {number}
"""

# Predict
async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not users.get(user_id):
        await update.message.reply_text("🔐 Enter Password First")
        return

    text = generate()

    keyboard = [[InlineKeyboardButton("Play Again 🎯", callback_data="again")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# ✅ Play Again FIX (NEW MESSAGE)
async def again(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = generate()

    keyboard = [[InlineKeyboardButton("Play Again 🎯", callback_data="again")]]

    # 👉 NEW MESSAGE (edit nahi hoga)
    await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# Run bot
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("predict", predict))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_password))
app.add_handler(CallbackQueryHandler(again))

print("✅ Bot running...")
app.run_polling()
