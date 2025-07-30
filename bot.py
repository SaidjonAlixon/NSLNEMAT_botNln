import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler
from sheets_handler import SheetsHandler
from pdf_generator import PDFGenerator
from config import TELEGRAM_BOT_TOKEN
import os
from id_storage import IDStorage

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
        self.id_storage = IDStorage()
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Start komandasi - har doim asosiy menyuga qaytadi"""
        user = update.effective_user
        
        # Foydalanuvchi ma'lumotlarini saqlash
        context.user_data['user_id'] = user.id
        context.user_data['username'] = user.username
        
        # Foydalanuvchining ro'yxatdan o'tganligini tekshirish
        if self.sheets_handler.is_user_registered(user.id):
            # Ro'yxatdan o'tgan foydalanuvchi - asosiy menyuga o'tish
            await update.message.reply_text(
                "🔄 Bot yangilandi!\n\n"
                "Assalomu alaykum! NE'MAT LASER SERVICE botiga xush kelibsiz!"
            )
            return await self.show_main_menu(update, context)
        else:
            # Ro'yxatdan o'tish jarayonini boshlash
            await update.message.reply_text(
                "Assalomu alaykum!\n"
                "NE'MAT LASER SERVICE botiga xush kelibsiz!\n\n"
                "Botdan foydalanish uchun avval ro'yxatdan o'ting.\n"
                "Ism kiriting:"
            )
            return NAME
    
    async def get_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Foydalanuvchi ismini olish"""
        context.user_data['name'] = update.message.text
        
        # Telefon raqamini so'rash
        keyboard = [[KeyboardButton("📞 Telefon raqamini ulash", request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        
        await update.message.reply_text(
            "Telefon raqamingizni ulashing:",
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
            "Kompaniya nomini kiriting:",
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
            context.user_data['business'],
            context.user_data['user_id']
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
            ["🔍 Buyurtmani tekshirish"],
            ["📦 Buyurtmalar tarixi"]
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
        telegram_id = update.effective_user.id
        if text == "🔍 Buyurtmani tekshirish":
            last_id = self.id_storage.get_client_id(telegram_id)
            if last_id:
                inline_keyboard = [[InlineKeyboardButton(f"{last_id}", callback_data=f"show_unfinished_{last_id}")]]
                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await update.message.reply_text(
                    "ID raqamingiz:",
                    reply_markup=inline_markup
                )
                return MAIN_MENU
            else:
                await update.message.reply_text(
                    "Iltimos, ID raqamingizni kiriting (masalan: NLS705464):"
                )
                return CHECK_ORDER
        elif text == "📌 Biz haqimizda":
            about_text = (
                "\U0001F3E2 NE'MAT LASER SERVICE\n\n"
                "Biz lazerli kesish va ishlab chiqarish xizmatlarini taqdim etamiz.\n\n"
                "\U0001F4DE Aloqa: \n"
                "+998 99 022 50 50 \n"
                "+998 97 002 77 77 \n"
                "+998 99 044 20 20 \n"
                "+998 99 844 20 20\n\n"
                "\U0001F4CD Manzil: г. Ташкент, район Сергели , ул. Саадий 87\n"
                "\U0001F552 Ish vaqti: Dushanba-Shanba 9:00-18:00"
            )
            await update.message.reply_text(about_text)
            return MAIN_MENU
        elif text == "📦 Buyurtmalar tarixi":
            last_id = self.id_storage.get_client_id(telegram_id)
            if last_id:
                inline_keyboard = [[InlineKeyboardButton(f"ID: {last_id} bo‘yicha ko‘rish", callback_data=f"show_completed_{last_id}")]]
                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await update.message.reply_text(
                    "Buyurtmalar tarixini ko‘rish uchun ID tugmasini bosing:",
                    reply_markup=inline_markup
                )
                return MAIN_MENU
            else:
                await update.message.reply_text(
                    "Iltimos, ID raqamingizni kiriting:"
                )
                return ORDER_HISTORY
        
        return MAIN_MENU
    
    async def check_order(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Buyurtmani tekshirish (yakunlanmaganlar ro'yxati, o'zbekcha, emoji bilan)"""
        telegram_id = update.effective_user.id
        client_id = update.message.text.strip()
        if client_id:
            self.id_storage.set_client_id(telegram_id, client_id)
        else:
            client_id = self.id_storage.get_client_id(telegram_id)
        if not client_id:
            await update.message.reply_text("Iltimos, ID kiriting!")
            return await self.show_main_menu(update, context)
        orders = self.sheets_handler.find_unfinished_orders_by_id(client_id)
        if not orders:
            # Xabar chiqarmaslik, faqat menyuga qaytish
            return await self.show_main_menu(update, context)
        for order in orders:
            message = (
                f"\U0001F4C5 Boshlangan sana: {order['start_date']}\n"
                f"\U0001F4DD Buyurtma: {order['project_name']}\n"
                f"\U0001F464 Mijoz: {order['client_name']}\n\n"
                f"\U0001F3A8 Dizayn: {'Tayyor' if order['designer'] == 'TRUE' else 'Tayyorlanmoqda'}\n"
                f"\U0001F526 Lazerli kesish: {'Tayyor' if order['laser_cutting'] == 'TRUE' else 'Tayyorlanmoqda'}\n"
                f"\U0001F52A Kesish: {'Tayyor' if order['cutting'] == 'TRUE' else 'Tayyorlanmoqda'}\n"
                f"\U0001F9FD Gubka: {'Tayyor' if order['sponge'] == 'TRUE' else 'Tayyorlanmoqda'}\n\n"
                f"\U0001F4CA Holat: {order['status']}% tayyor"
            )
            await update.message.reply_text(message)
        last_id = self.id_storage.get_client_id(telegram_id)
        if last_id:
            inline_keyboard = [[InlineKeyboardButton(f"ID: {last_id} bo‘yicha ko‘rish", callback_data=f"show_unfinished_{last_id}")]]
            inline_markup = InlineKeyboardMarkup(inline_keyboard)
            await update.message.reply_text("Oxirgi ishlatilgan ID:", reply_markup=inline_markup)
        return await self.show_main_menu(update, context)
    
    async def order_history(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Buyurtmalar tarixini ko'rsatish"""
        client_id = update.message.text.strip()
        context.user_data['last_id'] = client_id
        
        # Buyurtmalarni topish
        orders = self.sheets_handler.find_completed_orders_by_id(client_id)
        
        if not orders:
            await update.message.reply_text(
                "❌ Bu ID bo'yicha tugallangan buyurtmalar topilmadi!"
            )
            # Inline tugma chiqarish
            last_id = context.user_data.get('last_id')
            if last_id:
                inline_keyboard = [[InlineKeyboardButton(f"ID: {last_id} bo‘yicha ko‘rish", callback_data=f"show_completed_{last_id}")]]
                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await update.message.reply_text("Oxirgi ishlatilgan ID:", reply_markup=inline_markup)
            return await self.show_main_menu(update, context)
        
        # Buyurtmalar tarixini tayyorlash
        message = f"""📦 Tugallangan buyurtmalar soni: {len(orders)} ta\n"""
        
        # PDF faylini yaratish va loglar
        pdf_filename = self.pdf_generator.generate_completed_orders_pdf(orders)
        print("PDF filename:", pdf_filename)
        if pdf_filename and os.path.exists(pdf_filename):
            print("PDF exists, sending...")
            with open(pdf_filename, 'rb') as pdf_file:
                await update.message.reply_document(
                    document=pdf_file,
                    filename=f"tugallangan_buyurtmalar_{client_id}.pdf",
                    caption=message
                )
            os.remove(pdf_filename)
        else:
            print("PDF file not created or not found!")
        
        await update.message.reply_text(message)
        
        # Inline tugma chiqarish
        last_id = context.user_data.get('last_id')
        if last_id:
            inline_keyboard = [[InlineKeyboardButton(f"ID: {last_id} bo‘yicha ko‘rish", callback_data=f"show_completed_{last_id}")]]
            inline_markup = InlineKeyboardMarkup(inline_keyboard)
            await update.message.reply_text("Oxirgi ishlatilgan ID:", reply_markup=inline_markup)
        return await self.show_main_menu(update, context)
    
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Conversation ni bekor qilish"""
        await update.message.reply_text(
            "Bot ishlatish bekor qilindi.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    async def handle_inline_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        data = query.data
        if data.startswith("show_unfinished_"):
            client_id = data.replace("show_unfinished_", "")
            orders = self.sheets_handler.find_unfinished_orders_by_id(client_id)
            if not orders:
                await query.edit_message_text("❌ Siz kiritgan ID bo'yicha yakunlanmagan buyurtmalar topilmadi!")
            else:
                for order in orders:
                    message = (
                        f"\U0001F4C5 Boshlangan sana: {order['start_date']}\n"
                        f"\U0001F4DD Buyurtma: {order['project_name']}\n"
                        f"\U0001F464 Mijoz: {order['client_name']}\n\n"
                        f"\U0001F3A8 Dizayn: {'Tayyor' if order['designer'] == 'TRUE' else 'Tayyorlanmoqda'}\n"
                        f"\U0001F526 Lazerli kesish: {'Tayyor' if order['laser_cutting'] == 'TRUE' else 'Tayyorlanmoqda'}\n"
                        f"\U0001F52A Kesish: {'Tayyor' if order['cutting'] == 'TRUE' else 'Tayyorlanmoqda'}\n"
                        f"\U0001F9FD Gubka: {'Tayyor' if order['sponge'] == 'TRUE' else 'Tayyorlanmoqda'}\n\n"
                        f"\U0001F4CA Holat: {order['status']}% tayyor"
                    )
                    await query.message.reply_text(message)
        elif data.startswith("show_completed_"):
            client_id = data.replace("show_completed_", "")
            orders = self.sheets_handler.find_completed_orders_by_id(client_id)
            if not orders:
                await query.edit_message_text("❌ Siz kiritgan ID bo'yicha tugallangan buyurtmalar topilmadi!")
            else:
                # PDF generatsiya va yuborish
                pdf_filename = self.pdf_generator.generate_completed_orders_pdf(orders)
                if pdf_filename:
                    with open(pdf_filename, "rb") as pdf_file:
                        await query.message.reply_document(pdf_file, filename=pdf_filename)
                else:
                    await query.message.reply_text("PDF yaratishda xatolik yuz berdi!")
        return MAIN_MENU

    async def clear_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        telegram_id = update.effective_user.id
        self.id_storage.delete_client_id(telegram_id)
        await update.message.reply_text("ID o‘chirildi. Endi yangi ID kiritishingiz mumkin.")

def main():
    """Asosiy funksiya"""
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
    application.add_handler(CallbackQueryHandler(bot.handle_inline_id))
    application.add_handler(CommandHandler("clearid", bot.clear_id))
    
    # Botni ishga tushirish
    print("Bot ishga tushdi...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 