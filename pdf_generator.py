from fpdf import FPDF
from datetime import datetime
import os

class PDFGenerator:
    def __init__(self):
        pass

    def generate_completed_orders_pdf(self, orders):
        """Tugallangan buyurtmalar uchun PDF yaratish (faqat krilcha va rangli, ID va Тугаш муддати yo'q)"""
        try:
            pdf = FPDF()
            pdf.add_page()
            # DejaVuSans va DejaVuSans-Bold shriftlarini ulash
            font_path_regular = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
            font_path_bold = os.path.join(os.path.dirname(__file__), "DejaVuSans-Bold.ttf")
            if not os.path.exists(font_path_regular) or not os.path.exists(font_path_bold):
                print("DejaVuSans.ttf va DejaVuSans-Bold.ttf shriftlarini papkaga joylang!")
                return None
            pdf.add_font("DejaVu", "", font_path_regular, uni=True)
            pdf.add_font("DejaVu", "B", font_path_bold, uni=True)
            pdf.set_font("DejaVu", size=12)

            # Sarlavha
            pdf.set_fill_color(30, 144, 255)  # Ko'k
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("DejaVu", "B", 16)
            pdf.cell(0, 12, "NEMAT LASER SERVICE", ln=True, align='C', fill=True)
            pdf.set_font("DejaVu", "B", 14)
            pdf.cell(0, 10, "Тугалланган буюртмалар", ln=True, align='C', fill=True)
            pdf.ln(4)

            # Buyurtmalar soni
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("DejaVu", "B", 12)
            pdf.cell(0, 8, f"Тугалланган буюртмалар сони: {len(orders)} та", ln=True)
            pdf.ln(2)

            # Buyurtmalar ro'yxati
            for i, order in enumerate(orders, 1):
                pdf.set_fill_color(220, 230, 241)  # Yengil ko'k fon
                pdf.set_font("DejaVu", "B", 11)
                pdf.cell(0, 7, f"{i}-буюртма", ln=True, fill=True)
                pdf.set_font("DejaVu", "", 10)
                pdf.set_text_color(0, 0, 0)
                # pdf.cell(0, 6, f"ID: {order['client_id']}", ln=True)  # ID chiqarilmaydi
                pdf.cell(0, 6, f"Сана: {order['start_date']}", ln=True)
                pdf.cell(0, 6, f"Мижоз: {order['client_name']}", ln=True)
                # Mahsulot nomini qisqartirish
                project_name = order['project_name']
                if len(project_name) > 60:
                    project_name = project_name[:60] + "..."
                pdf.cell(0, 6, f"Маҳсулот: {project_name}", ln=True)
                # Statuslar
                pdf.set_font("DejaVu", "B", 10)
                pdf.cell(0, 6, "Ишлаб чиқариш ҳолати:", ln=True)
                pdf.set_font("DejaVu", "", 10)
                pdf.cell(0, 6, f"Дизайн: {'Тайёр' if order['designer'] == 'TRUE' else 'Тайёрланмоқда'}", ln=True)
                pdf.cell(0, 6, f"Лазерли кесиш: {'Тайёр' if order['laser_cutting'] == 'TRUE' else 'Тайёрланмоқда'}", ln=True)
                pdf.cell(0, 6, f"Кесиш: {'Тайёр' if order['cutting'] == 'TRUE' else 'Тайёрланмоқда'}", ln=True)
                pdf.cell(0, 6, f"Губка: {'Тайёр' if order['sponge'] == 'TRUE' else 'Тайёрланмоқда'}", ln=True)
                pdf.cell(0, 6, f"Статус: {order['status']}% тайёр", ln=True)
                # if order['sent_date']:
                #     pdf.cell(0, 6, f"Тугаш муддати: {order['sent_date']}", ln=True)  # Тугаш муддати chiqarilmaydi
                pdf.ln(2)
                # Ajratkich
                pdf.set_draw_color(100, 100, 100)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(2)

            # PDF faylini saqlash
            filename = f"completed_orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf.output(filename)
            return filename

        except Exception as e:
            print(f"PDF yaratishda xatolik: {e}")
            return None

    def generate_order_pdf(self, order_data):
        """Buyurtma ma'lumotlari uchun PDF yaratish"""
        try:
            self.pdf = FPDF()
            self.pdf.add_page()
            self.pdf.set_font("Arial", size=12)
            
            # Sarlavha
            self.pdf.cell(200, 10, txt="NEMAT LASER SERVICE", ln=True, align='C')
            self.pdf.cell(200, 10, txt="Buyurtma ma'lumotlari", ln=True, align='C')
            self.pdf.ln(10)
            
            # Ma'lumotlar
            self.pdf.set_font("Arial", 'B', 12)
            self.pdf.cell(200, 10, txt=f"Buyurtma ID: {order_data['client_id']}", ln=True)
            self.pdf.cell(200, 10, txt=f"Boshlangan sana: {order_data['start_date']}", ln=True)
            
            # Buyurtma nomini qisqartirish
            project_name = order_data['project_name']
            if len(project_name) > 50:
                project_name = project_name[:50] + "..."
            self.pdf.cell(200, 10, txt=f"Buyurtma: {project_name}", ln=True)
            self.pdf.cell(200, 10, txt=f"Mijoz Ism familiyasi: {order_data['client_name']}", ln=True)
            self.pdf.ln(5)
            
            # Status ma'lumotlari
            self.pdf.set_font("Arial", 'B', 12)
            self.pdf.cell(200, 10, txt="Ishlab chiqarish holati:", ln=True)
            self.pdf.set_font("Arial", size=12)
            
            # Dizayn statusi
            designer_status = "Tayyor" if order_data['designer'] == 'TRUE' else "Tayyorlanmoqda"
            self.pdf.cell(200, 10, txt=f"Dizayn: {designer_status}", ln=True)
            
            # Lazerli kesish statusi
            laser_status = "Tayyor" if order_data['laser_cutting'] == 'TRUE' else "Tayyorlanmoqda"
            self.pdf.cell(200, 10, txt=f"Lazerli kesish: {laser_status}", ln=True)
            
            # Kesish statusi
            cutting_status = "Tayyor" if order_data['cutting'] == 'TRUE' else "Tayyorlanmoqda"
            self.pdf.cell(200, 10, txt=f"Kesish: {cutting_status}", ln=True)
            
            # Gubka statusi
            sponge_status = "Tayyor" if order_data['sponge'] == 'TRUE' else "Tayyorlanmoqda"
            self.pdf.cell(200, 10, txt=f"Gubka: {sponge_status}", ln=True)
            
            self.pdf.ln(5)
            
            # Umumiy holat
            self.pdf.set_font("Arial", 'B', 12)
            self.pdf.cell(200, 10, txt=f"Holat: {order_data['status']}% tayyor", ln=True)
            
            # Yuborilgan sana
            if order_data['sent_date']:
                self.pdf.cell(200, 10, txt=f"Zakaz tugash muddati: {order_data['sent_date']}", ln=True)
            else:
                self.pdf.cell(200, 10, txt="Zakaz tugash muddati: tez fursatda tayyor bo'ladi", ln=True)
            
            # PDF faylini saqlash
            filename = f"order_{order_data['client_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            self.pdf.output(filename)
            return filename
            
        except Exception as e:
            print(f"PDF yaratishda xatolik: {e}")
            return None
    
    def generate_orders_history_pdf(self, client_name, orders):
        """Buyurtmalar tarixi uchun PDF yaratish"""
        try:
            self.pdf = FPDF()
            self.pdf.add_page()
            self.pdf.set_font("Arial", 'B', 16)
            
            # Sarlavha
            self.pdf.cell(200, 10, txt="NEMAT LASER SERVICE", ln=True, align='C')
            self.pdf.cell(200, 10, txt="Buyurtmalar tarixi", ln=True, align='C')
            self.pdf.ln(10)
            
            # Mijoz ma'lumotlari
            self.pdf.set_font("Arial", 'B', 14)
            self.pdf.cell(200, 10, txt=f"Ism: {client_name}", ln=True)
            self.pdf.cell(200, 10, txt=f"Zakazlar soni: {len(orders)} ta", ln=True)
            self.pdf.ln(10)
            
            # Buyurtmalar ro'yxati
            for i, order in enumerate(orders, 1):
                self.pdf.set_font("Arial", 'B', 12)
                self.pdf.cell(200, 10, txt=f"{i}.", ln=True)
                
                self.pdf.set_font("Arial", size=12)
                self.pdf.cell(200, 10, txt=f"ID: {order['client_id']}", ln=True)
                self.pdf.cell(200, 10, txt=f"Sana: {order['start_date']}", ln=True)
                
                # Mahsulot nomini qisqartirish
                project_name = order['project_name']
                if len(project_name) > 50:
                    project_name = project_name[:50] + "..."
                self.pdf.cell(200, 10, txt=f"Mahsulot: {project_name}", ln=True)
                self.pdf.cell(200, 10, txt=f"Status: {order['status']}% tayyor", ln=True)
                self.pdf.ln(5)
            
            # PDF faylini saqlash
            filename = f"history_{client_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            self.pdf.output(filename)
            return filename
            
        except Exception as e:
            print(f"PDF yaratishda xatolik: {e}")
            return None 