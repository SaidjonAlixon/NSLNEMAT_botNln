import os
import logging
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from sheets_handler import SheetsHandler
from pdf_generator import PDFGenerator
from config import TELEGRAM_BOT_TOKEN

# Logging sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
NAME, PHONE, BUSINESS, MAIN_MENU, CHECK_ORDER, ORDER_HISTORY = range(6)

class NematLaserBot:
    def __init__(self):
        self.sheets_handler = SheetsHandler()
        self.pdf_generator = PDFGenerator()
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Start komandasi"""
        user = update.effective_user
        
        # Foydalanuvchi ma'lumotlarini saqlash
        context.user_data['user_id'] = user.id
        context.user_data['username'] = user.username
        
        await update.message.reply_text(
            "Assalomu alaykum! NE'MAT LASER SERVICE botiga xush kelibsiz!\n\n"
            "Botdan foydalanish uchun avval ro'yxatdan o'tishingiz kerak.\n\n"
            "Iltimos, ism va familiyangizni kiriting:"
        )
        return NAME
    
    async def get_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Foydalanuvchi ismini olish"""
        context.user_data['name'] = update.message.text
        
        # Telefon raqamini so'rash
        keyboard = [[KeyboardButton("📞 Telefon raqamini ulash", request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        
        await update.message.reply_text(
            "Iltimos, telefon raqamingizni ulashing:",
            reply_markup=reply_markup
        )
        return PHONE
    
    async def get_phone(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Telefon raqamini olish"""
        if update.message.contact:
            context.user_data['phone'] = update.message.contact.phone_number
        else:
            context.user_data['phone'] = update.message.text
        
        await update.message.reply_text(
            "Iltimos, biznes nomingizni kiriting:",
            reply_markup=ReplyKeyboardRemove()
        )
        return BUSINESS
    
    async def get_business(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Biznes nomini olish va ma'lumotlarni saqlash"""
        context.user_data['business'] = update.message.text
        
        # Ma'lumotlarni Google Sheets ga saqlash
        success = self.sheets_handler.add_user(
            context.user_data['name'],
            context.user_data['phone'],
            context.user_data['business']
        )
        
        if success:
            await update.message.reply_text(
                "✅ Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!\n\n"
                "Assalomu alaykum, xush kelibsiz!\n"
                "NE'MAT LASER SERVICE botiga!"
            )
        else:
            await update.message.reply_text(
                "❌ Ro'yxatdan o'tishda xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."
            )
        
        return await self.show_main_menu(update, context)
    
    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Asosiy menyuni ko'rsatish"""
        keyboard = [
            ["📌 Biz haqimizda"],
            ["🔍 Zakazni tekshirish"],
            ["📦 Umumiy zakazlar tarixi"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            "Asosiy menyu:",
            reply_markup=reply_markup
        )
        return MAIN_MENU
    
    async def handle_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Asosiy menyu tugmalarini boshqarish"""
        text = update.message.text
        
        if text == "📌 Biz haqimizda":
            await update.message.reply_text(
                "🏢 NE'MAT LASER SERVICE\n\n"
                "Biz lazerli kesish va ishlab chiqarish xizmatlarini taqdim etamiz.\n\n"
                "📞 Aloqa: +998 XX XXX XX XX\n"
                "📍 Manzil: Toshkent shahri\n"
                "🕒 Ish vaqti: Dushanba-Shanba 9:00-18:00"
            )
            return MAIN_MENU
            
        elif text == "🔍 Zakazni tekshirish":
            await update.message.reply_text(
                "Iltimos, Kilent ID raqamingizni kiriting (masalan: NLS705464):"
            )
            return CHECK_ORDER
            
        elif text == "📦 Umumiy zakazlar tarixi":
            await update.message.reply_text(
                "Iltimos, Ism va Familiyangizni kiriting:"
            )
            return ORDER_HISTORY
        
        return MAIN_MENU
    
    async def check_order(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Buyurtmani tekshirish"""
        client_id = update.message.text.strip()
        
        # Buyurtmani topish
        order = self.sheets_handler.find_order_by_id(client_id)
        
        if not order:
            await update.message.reply_text(
                "❌ Siz noto'g'ri ID yubordingiz!\n\n"
                "Iltimos, to'g'ri Kilent ID raqamini kiriting."
            )
            return CHECK_ORDER
        
        # Buyurtma ma'lumotlarini tayyorlash
        message = f"""📦 Buyurtma ma'lumotlari:

📦 Buyurtma ID: {order['client_id']}
📅 Boshlangan sana: {order['start_date']}
📝 Buyurtma: {order['project_name']}
👤 Mijoz Ism familiyasi: {order['client_name']}

🎨 Dizayn: {'Tayyor' if order['designer'] == 'TRUE' else 'Tayyorlanmoqda'}
🔦 Lazerli kesish: {'Tayyor' if order['laser_cutting'] == 'TRUE' else 'Tayyorlanmoqda'}
🔪 Kesish: {'Tayyor' if order['cutting'] == 'TRUE' else 'Tayyorlanmoqda'}
🧽 Gubka: {'Tayyor' if order['sponge'] == 'TRUE' else 'Tayyorlanmoqda'}

📊 Holat: {order['status']}% tayyor"""

        # Yuborilgan sana
        if order['sent_date']:
            message += f"\n📤 Zakaz tugash muddati: {order['sent_date']}"
        else:
            message += "\n📤 Zakaz tugash muddati: tez fursatda tayyor bo'ladi"
        
        await update.message.reply_text(message)
        
        # PDF faylini yaratish va yuborish
        pdf_filename = self.pdf_generator.generate_order_pdf(order)
        if pdf_filename and os.path.exists(pdf_filename):
            with open(pdf_filename, 'rb') as pdf_file:
                await update.message.reply_document(
                    document=pdf_file,
                    filename=f"buyurtma_{order['client_id']}.pdf",
                    caption="📄 Buyurtma ma'lumotlari PDF fayli"
                )
            # PDF faylini o'chirish
            os.remove(pdf_filename)
        
        return await self.show_main_menu(update, context)
    
    async def order_history(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Buyurtmalar tarixini ko'rsatish"""
        client_name = update.message.text.strip()
        
        # Buyurtmalarni topish
        orders = self.sheets_handler.find_orders_by_name(client_name)
        
        if not orders:
            await update.message.reply_text(
                "❌ Bu ism bilan hech qanday buyurtma topilmadi!\n\n"
                "Iltimos, to'g'ri ism va familiyangizni kiriting."
            )
            return ORDER_HISTORY
        
        # Buyurtmalar tarixini tayyorlash
        message = f"""👤 Ism: {client_name}
📦 Zakazlar soni: {len(orders)} ta

"""
        
        for i, order in enumerate(orders, 1):
            message += f"""{i}️⃣
🆔: {order['client_id']}
📅 Sana: {order['start_date']}
📝 Mahsulot: {order['project_name']}
📊 Status: {order['status']}% tayyor

"""
        
        await update.message.reply_text(message)
        
        # PDF faylini yaratish va yuborish
        pdf_filename = self.pdf_generator.generate_orders_history_pdf(client_name, orders)
        if pdf_filename and os.path.exists(pdf_filename):
            with open(pdf_filename, 'rb') as pdf_file:
                await update.message.reply_document(
                    document=pdf_file,
                    filename=f"buyurtmalar_tarixi_{client_name}.pdf",
                    caption="📄 Buyurtmalar tarixi PDF fayli"
                )
            # PDF faylini o'chirish
            os.remove(pdf_filename)
        
        return await self.show_main_menu(update, context)
    
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Conversation ni bekor qilish"""
        await update.message.reply_text(
            "Bot ishlatish bekor qilindi.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

# Flask app yaratish
app = Flask(__name__)

# Bot yaratish
bot = NematLaserBot()

# Application yaratish
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# Conversation handler
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", bot.start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_name)],
        PHONE: [MessageHandler(filters.CONTACT | filters.TEXT & ~filters.COMMAND, bot.get_phone)],
        BUSINESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_business)],
        MAIN_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_main_menu)],
        CHECK_ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.check_order)],
        ORDER_HISTORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.order_history)],
    },
    fallbacks=[CommandHandler("cancel", bot.cancel)],
)

application.add_handler(conv_handler)

@app.route('/')
def home():
    return jsonify({
        "status": "success",
        "message": "NE'MAT LASER SERVICE Bot ishlayapti!",
        "bot": "Telegram Bot ishlayapti"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "bot": "running"
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Telegram webhook"""
    try:
        update = Update.de_json(request.get_json(), application.bot)
        application.process_update(update)
        return jsonify({"status": "ok"})
    except Exception as e:
        logger.error(f"Webhook xatolik: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

def main():
    """Asosiy funksiya"""
    port = int(os.environ.get('PORT', 5000))
    
    # Railway da webhook o'rnatish
    if os.environ.get('RAILWAY_ENVIRONMENT'):
        # Webhook URL ni o'rnatish
        webhook_url = f"https://{os.environ.get('RAILWAY_STATIC_URL')}/webhook"
        application.bot.set_webhook(url=webhook_url)
        logger.info(f"Webhook o'rnatildi: {webhook_url}")
    
    # Flask app ni ishga tushirish
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    main() 