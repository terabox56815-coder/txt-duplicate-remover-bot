import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ["BOT_TOKEN"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📄 TXT Duplicate Remover Bot\n\nTXT ফাইল পাঠান।"
    )

async def process_txt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document

    if not doc.file_name.lower().endswith(".txt"):
        await update.message.reply_text("শুধু TXT ফাইল পাঠান")
        return

    file = await context.bot.get_file(doc.file_id)
    input_file = f"{doc.file_unique_id}.txt"

    await file.download_to_drive(input_file)

    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        lines = [x.strip() for x in f if x.strip()]

    unique = list(dict.fromkeys(lines))

    output_file = f"cleaned_{doc.file_unique_id}.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(unique))

    await update.message.reply_document(
        document=open(output_file, "rb"),
        filename=f"cleaned_{doc.file_name}",
        caption=f"✅ Total: {len(lines)}\n✨ Unique: {len(unique)}\n🗑 Removed: {len(lines)-len(unique)}"
    )

    os.remove(input_file)
    os.remove(output_file)

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Document.ALL, process_txt))

app.run_polling()
