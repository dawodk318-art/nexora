import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("NEXORA_BOT_TOKEN")
WEB_APP_URL = os.environ.get("NEXORA_WEB_APP_URL")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))
if not TOKEN:
    raise RuntimeError("NEXORA_BOT_TOKEN is not set.")

if not WEB_APP_URL or not WEB_APP_URL.startswith("https://"):
    raise RuntimeError("NEXORA_WEB_APP_URL is not set correctly.")


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Nexora bot is running!")

    def log_message(self, format, *args):
        pass


def start_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton(
            "🚀 PLAY NEXORA",
            web_app={"url": WEB_APP_URL}
        )
    ]]

    await update.message.reply_text(
        "🌟 Welcome to NEXORA! 🌟\n\n"
        "Tap the coin, earn NEX points and upgrade your power.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ You are not authorized.")
        return

    keyboard = [
        [
            InlineKeyboardButton("👥 Players", callback_data="admin_players"),
            InlineKeyboardButton("📊 Stats", callback_data="admin_stats")
        ],
        [
            InlineKeyboardButton("🏆 Leaderboard", callback_data="admin_leaderboard"),
            InlineKeyboardButton("⚙️ Settings", callback_data="admin_settings")
        ]
    ]

    await update.message.reply_text(
        "🛡️ NEXORA ADMIN PANEL\n\n"
        "Welcome, Admin.\n"
        "Choose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def main():
    threading.Thread(
        target=start_health_server,
        daemon=True
    ).start()

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
app.add_handler(CommandHandler("admin", admin))
    print("Nexora bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
