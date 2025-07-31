import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from config import GOOGLE_SHEETS_ID, ORDERS_SHEET, USERS_SHEET
import os
import json

class SheetsHandler:
    def __init__(self):
        # Google Sheets API uchun ruxsatlar
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # Service account credentials
        if os.getenv('GOOGLE_CREDENTIALS'):
            # Railway da environment variable dan o'qish
            creds_dict = json.loads(os.getenv('GOOGLE_CREDENTIALS'))
            creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        else:
            # Local development uchun config.json faylidan o'qish
            creds = Credentials.from_service_account_file('config.json', scopes=scope)
        
        self.client = gspread.authorize(creds)
        
        # Spreadsheet ochish
        self.spreadsheet = self.client.open_by_key(GOOGLE_SHEETS_ID)
        
        # Worksheet nomlarini tekshirish
        self._check_worksheets()
        
    def _check_worksheets(self):
        """Worksheet nomlarini tekshirish va mavjud worksheetlarni ko'rsatish"""
        try:
            worksheets = self.spreadsheet.worksheets()
            print(f"Mavjud worksheetlar:")
            for ws in worksheets:
                print(f"- {ws.title}")
            
            # Worksheet nomlarini to'g'rilash
            self.orders_sheet_name = None
            self.users_sheet_name = None
            
            # Avval aniq nomlar bilan qidiramiz
            for ws in worksheets:
                if ws.title == ORDERS_SHEET or ws.title == "List1 - buyurtmalar":
                    self.orders_sheet_name = ws.title
                elif ws.title == USERS_SHEET or ws.title == "List3 - ro'yxatdan o'tganlar":
                    self.users_sheet_name = ws.title
            
            # Agar topilmasa, qismiy nomlar bilan qidiramiz
            if not self.orders_sheet_name:
                for ws in worksheets:
                    if "list1" in ws.title.lower() or "buyurtmalar" in ws.title.lower():
                        self.orders_sheet_name = ws.title
                        break
            
            if not self.users_sheet_name:
                for ws in worksheets:
                    if "list3" in ws.title.lower() or "ro'yxatdan" in ws.title.lower():
                        self.users_sheet_name = ws.title
                        break
            
            # Agar hali ham topilmasa, birinchi worksheetlarni olamiz
            if not self.orders_sheet_name and len(worksheets) >= 1:
                self.orders_sheet_name = worksheets[0].title
                print(f"Buyurtmalar uchun birinchi worksheet ishlatiladi: {self.orders_sheet_name}")
            
            if not self.users_sheet_name and len(worksheets) >= 2:
                self.users_sheet_name = worksheets[1].title
                print(f"Foydalanuvchilar uchun ikkinchi worksheet ishlatiladi: {self.users_sheet_name}")
            
            print(f"Buyurtmalar worksheet: {self.orders_sheet_name}")
            print(f"Foydalanuvchilar worksheet: {self.users_sheet_name}")
            
        except Exception as e:
            print(f"Worksheet nomlarini tekshirishda xatolik: {e}")
    
    def is_user_registered(self, telegram_id):
        """Telegram ID bo'yicha foydalanuvchi ro'yxatdan o'tganligini tekshirish"""
        try:
            if not self.users_sheet_name:
                print("Foydalanuvchilar worksheet topilmadi!")
                return False
                
            worksheet = self.spreadsheet.worksheet(self.users_sheet_name)
            all_values = worksheet.get_all_values()
            
            # E ustunda Telegram ID saqlanadi
            for row in all_values[1:]:  # Header qatorini o'tkazib yuborish
                if len(row) > 4 and str(row[4]) == str(telegram_id):
                    return True
            return False
        except Exception as e:
            print(f"Foydalanuvchi tekshirishda xatolik: {e}")
            return False
        
    def add_user(self, name, phone, business, telegram_id=None):
        """Yangi foydalanuvchini qo'shish"""
        try:
            if not self.users_sheet_name:
                print("Foydalanuvchilar worksheet topilmadi!")
                return False
                
            worksheet = self.spreadsheet.worksheet(self.users_sheet_name)
            today = datetime.now().strftime('%d.%m.%Y')
            
            # Yangi qator qo'shish (A: Ism, B: Telefon, C: Biznes, D: Sana, E: Telegram ID)
            row = [name, phone, business, today, telegram_id if telegram_id else '']
            worksheet.append_row(row)
            print(f"Foydalanuvchi muvaffaqiyatli qo'shildi: {name}")
            return True
        except Exception as e:
            print(f"Foydalanuvchi qo'shishda xatolik: {e}")
            return False
    
    def find_order_by_id(self, client_id):
        """Client ID bo'yicha buyurtmani topish"""
        try:
            if not self.orders_sheet_name:
                print("Buyurtmalar worksheet topilmadi!")
                return None
                
            worksheet = self.spreadsheet.worksheet(self.orders_sheet_name)
            all_values = worksheet.get_all_values()
            
            print(f"Jadvalda {len(all_values)} qator mavjud")
            
            # E ustun (Client ID) - 4-indeks
            for i, row in enumerate(all_values[4:], start=5):  # 5-qatordan boshlanadi
                if len(row) > 4 and row[4] == client_id:  # E ustun
                    print(f"Buyurtma topildi: {client_id}")
                    return {
                        'row': i,
                        'order_number': row[0] if len(row) > 0 else '',
                        'start_date': row[1] if len(row) > 1 else '',
                        'project_name': row[2] if len(row) > 2 else '',
                        'client_name': row[3] if len(row) > 3 else '',
                        'client_id': row[4] if len(row) > 4 else '',
                        'designer': row[5] if len(row) > 5 else '',
                        'laser_cutting': row[6] if len(row) > 6 else '',
                        'cutting': row[7] if len(row) > 7 else '',
                        'sponge': row[8] if len(row) > 8 else '',
                        'status': row[9] if len(row) > 9 else '',
                        'sent_checkbox': row[10] if len(row) > 10 else '',
                        'sent_date': row[11] if len(row) > 11 else ''
                    }
            
            print(f"Buyurtma topilmadi: {client_id}")
            return None
        except Exception as e:
            print(f"Buyurtma qidirishda xatolik: {e}")
            return None
    
    def find_completed_orders_by_id(self, client_id):
        """Client ID bo'yicha barcha tugallangan (status=100 va K yacheykada ptichka) buyurtmalarni topish"""
        try:
            if not self.orders_sheet_name:
                print("Buyurtmalar worksheet topilmadi!")
                return []
                
            worksheet = self.spreadsheet.worksheet(self.orders_sheet_name)
            all_values = worksheet.get_all_values()
            
            orders = []
            # E ustun (Client ID) - 4-indeks, J ustun (Status) - 9-indeks, K ustun (Sent Checkbox) - 10-indeks
            for i, row in enumerate(all_values[4:], start=5):  # 5-qatordan boshlanadi
                # Shartlar: E ustunda client_id, J ustunda 100, K ustunda TRUE yoki ✓
                k_value = row[10] if len(row) > 10 else ''
                if (len(row) > 10 and row[4] == client_id and row[9] == '100' and 
                    (k_value == 'TRUE' or k_value == '✓' or k_value.upper() == 'TRUE')):
                    order = {
                        'row': i,
                        'order_number': row[0] if len(row) > 0 else '',
                        'start_date': row[1] if len(row) > 1 else '',
                        'project_name': row[2] if len(row) > 2 else '',
                        'client_name': row[3] if len(row) > 3 else '',
                        'client_id': row[4] if len(row) > 4 else '',
                        'designer': row[5] if len(row) > 5 else '',
                        'laser_cutting': row[6] if len(row) > 6 else '',
                        'cutting': row[7] if len(row) > 7 else '',
                        'sponge': row[8] if len(row) > 8 else '',
                        'status': row[9] if len(row) > 9 else '',
                        'sent_date': row[11] if len(row) > 11 else ''
                    }
                    orders.append(order)
            
            print(f"{client_id} uchun {len(orders)} ta tugallangan va K yacheykada belgilangan buyurtma topildi")
            return orders
        except Exception as e:
            print(f"Tugallangan buyurtmalarni qidirishda xatolik: {e}")
            return []

    def find_orders_by_name(self, client_name):
        """Client nomi bo'yicha barcha buyurtmalarni topish"""
        try:
            if not self.orders_sheet_name:
                print("Buyurtmalar worksheet topilmadi!")
                return []
                
            worksheet = self.spreadsheet.worksheet(self.orders_sheet_name)
            all_values = worksheet.get_all_values()
            
            orders = []
            # D ustun (Client Name) - 3-indeks
            for i, row in enumerate(all_values[4:], start=5):  # 5-qatordan boshlanadi
                if len(row) > 3 and row[3] == client_name:  # D ustun
                    order = {
                        'row': i,
                        'order_number': row[0] if len(row) > 0 else '',
                        'start_date': row[1] if len(row) > 1 else '',
                        'project_name': row[2] if len(row) > 2 else '',
                        'client_name': row[3] if len(row) > 3 else '',
                        'client_id': row[4] if len(row) > 4 else '',
                        'designer': row[5] if len(row) > 5 else '',
                        'laser_cutting': row[6] if len(row) > 6 else '',
                        'cutting': row[7] if len(row) > 7 else '',
                        'status': row[9] if len(row) > 9 else '',
                        'sent_date': row[11] if len(row) > 11 else ''
                    }
                    orders.append(order)
            
            print(f"{client_name} uchun {len(orders)} ta buyurtma topildi")
            return orders
        except Exception as e:
            print(f"Buyurtmalar qidirishda xatolik: {e}")
            return [] 

    def find_unfinished_orders_by_id(self, client_id):
        """Client ID bo‘yicha statusi 100 bo‘lmagan barcha buyurtmalarni topish"""
        try:
            if not self.orders_sheet_name:
                print("Buyurtmalar worksheet topilmadi!")
                return []
            worksheet = self.spreadsheet.worksheet(self.orders_sheet_name)
            all_values = worksheet.get_all_values()
            orders = []
            for i, row in enumerate(all_values[4:], start=5):  # 5-qatordan boshlanadi
                if len(row) > 4 and row[4] == client_id:  # E ustun
                    status = row[9] if len(row) > 9 else ''
                    k_value = row[10] if len(row) > 10 else ''
                    
                    # Shartlar: status != 100 yoki (status = 100 lekin K yacheykada ptichka yo'q)
                    is_sent = (k_value == 'TRUE' or k_value == '✓' or k_value.upper() == 'TRUE')
                    
                    if status != '100' or (status == '100' and not is_sent):
                        order = {
                            'row': i,
                            'order_number': row[0] if len(row) > 0 else '',
                            'start_date': row[1] if len(row) > 1 else '',
                            'project_name': row[2] if len(row) > 2 else '',
                            'client_name': row[3] if len(row) > 3 else '',
                            'client_id': row[4] if len(row) > 4 else '',
                            'designer': row[5] if len(row) > 5 else '',
                            'laser_cutting': row[6] if len(row) > 6 else '',
                            'cutting': row[7] if len(row) > 7 else '',
                            'sponge': row[8] if len(row) > 8 else '',
                            'status': row[9] if len(row) > 9 else '',
                            'sent_date': row[11] if len(row) > 11 else ''
                        }
                        orders.append(order)
            print(f"{client_id} uchun {len(orders)} ta yakunlanmagan va K yacheykada belgilanmagan buyurtma topildi")
            return orders
        except Exception as e:
            print(f"Yakunlanmagan buyurtmalarni qidirishda xatolik: {e}")
            return [] 