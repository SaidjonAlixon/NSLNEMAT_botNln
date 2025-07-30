# NEMAT LASER SERVICE Telegram Bot

Bu bot NEMAT LASER SERVICE kompaniyasi uchun yaratilgan Telegram bot bo'lib, mijozlarga buyurtmalar holatini ko'rish, ma'lumotlarni qabul qilish va PDF holatda buyurtmani yuborish imkonini beradi.

## 🚀 Xususiyatlar

### 1. Ro'yxatdan o'tish
- Foydalanuvchi ismi va familiyasi
- Telefon raqami (Contact share tugmasi orqali)
- Biznes nomi
- Ma'lumotlar Google Sheets ga saqlanadi

### 2. Asosiy menyu
- 📌 Biz haqimizda
- 🔍 Buyurtmani tekshirish
- 📦 Buyurtmalar tarixi

### 3. Buyurtma tekshirish (Yakunlanmagan)
- Client ID bo'yicha qidirish (1 marta kiritiladi, doimiy saqlanadi)
- Statusi 100% bo'lmagan buyurtmalar
- Inline tugma orqali tez kirish
- Lotin alifbosida ma'lumot ko'rsatish

### 4. Buyurtmalar tarixi (Tugallangan)
- Client ID bo'yicha qidirish
- Faqat tugallangan buyurtmalar (status 100%)
- PDF fayl sifatida yuborish
- Krilcha va rangli PDF

## 📋 O'rnatish

### 1. Kerakli kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 2. Konfiguratsiya
1. `config.py` faylida Telegram bot tokenini o'rnating
2. Google Sheets ID ni o'rnating
3. `config.json` faylida Google Service Account ma'lumotlari mavjud

### 3. Google Sheets sozlash
1. Google Sheets da ikkita worksheet yarating:
   - "List1 - buyurtmalar" - buyurtmalar ma'lumotlari
   - "List3 - ro'yxatdan o'tganlar" - foydalanuvchilar ma'lumotlari

2. Google Service Account ga ruxsat bering

### 4. Botni ishga tushirish
```bash
python bot.py
```

## 🚀 GitHub va Railway Deployment

### GitHub ga Push qilish

1. **Git repository yaratish:**
```bash
git init
git add .
git commit -m "Initial commit: NEMAT LASER SERVICE Bot"
```

2. **GitHub da repository yaratish va push qilish:**
```bash
git remote add origin https://github.com/YOUR_USERNAME/nls-bot.git
git branch -M main
git push -u origin main
```

### Railway da Deployment

1. **Railway ga kirish:**
   - [Railway.app](https://railway.app) ga o'ting
   - GitHub account bilan tizimga kiring

2. **Yangi project yaratish:**
   - "New Project" tugmasini bosing
   - "Deploy from GitHub repo" ni tanlang
   - GitHub repositoryingizni tanlang

3. **Environment Variables o'rnatish:**
   Railway project settings da quyidagi environment variables qo'shing:

   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   GOOGLE_SHEETS_ID=your_google_sheets_id
   GOOGLE_CREDENTIALS={"type":"service_account","project_id":"...","private_key_id":"...","private_key":"...","client_email":"...","client_id":"...","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"..."}
   ORDERS_SHEET=List1
   USERS_SHEET=List3
   ```

   **Muhim:** ID saqlash uchun SQLite bazasi avtomatik yaratiladi (`user_ids.db`)

4. **Google Service Account ma'lumotlarini olish:**
   - Google Cloud Console ga o'ting
   - Service Account yarating
   - JSON key yuklab oling
   - JSON faylning ichidagi ma'lumotlarni `GOOGLE_CREDENTIALS` ga qo'shing

5. **Deployment:**
   - Railway avtomatik ravishda GitHub dan kodni o'qib, deployment qiladi
   - Deployment tugagandan so'ng, Railway sizga URL beradi

### Telegram Bot Webhook sozlash

Railway deployment tugagandan so'ng:

1. **Webhook URL ni olish:**
   - Railway project da "Settings" ga o'ting
   - "Domains" bo'limida URL ni ko'ring
   - Webhook URL: `https://your-app-name.railway.app/webhook`

2. **Telegram Bot API orqali webhook o'rnatish:**
```bash
curl -X POST "https://api.telegram.org/botYOUR_BOT_TOKEN/setWebhook" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://your-app-name.railway.app/webhook"}'
```

## 📁 Fayl strukturasi

```
├── app.py              # Railway uchun asosiy fayl
├── bot.py              # Local development uchun
├── sheets_handler.py   # Google Sheets bilan ishlash
├── pdf_generator.py    # PDF fayllarini yaratish
├── id_storage.py       # SQLite ID saqlash
├── config.py           # Konfiguratsiya
├── config.json         # Google Service Account (local)
├── DejaVuSans.ttf      # PDF font (Krilcha)
├── DejaVuSans-Bold.ttf # PDF bold font
├── requirements.txt    # Kerakli kutubxonalar
├── Procfile           # Railway deployment
├── runtime.txt        # Python versiyasi
├── .gitignore         # Git ignore fayllar
└── README.md          # Loyiha ma'lumoti
```

## 🔧 Texnik ma'lumotlar

- **Til:** Python 3.11+
- **Telegram Bot API:** python-telegram-bot 20.7
- **Google Sheets:** gspread 5.12.0
- **PDF:** fpdf2 2.7.6
- **Web Framework:** Flask 3.0.0
- **Deployment:** Railway

## 📊 Google Sheets strukturasi

### List1 - buyurtmalar
- A ustun: № (Buyurtma raqami)
- B ustun: Boshlangan kun
- C ustun: Proyektlar nomi
- D ustun: Mijoz I.F.Sh
- E ustun: Kilent ID
- F ustun: Dizayner (TRUE/FALSE)
- G ustun: Lazerli kesish (TRUE/FALSE)
- H ustun: Kesish (TRUE/FALSE)
- I ustun: Gubka (TRUE/FALSE)
- J ustun: Status (%)
- K ustun: Yuborilgan checkbox
- L ustun: Mijozga jo'natilgan sana

### List3 - ro'yxatdan o'tganlar
- A ustun: Ism
- B ustun: Telefon
- C ustun: Biznes
- D ustun: Sana

## 🎯 Bot ishlash tartibi

1. **Start** - Foydalanuvchi ro'yxatdan o'tadi
2. **Asosiy menyu** - Foydalanuvchi tanlov qiladi
3. **Buyurtma tekshirish** - Client ID kiritiladi (1 marta), keyingi safar inline tugma chiqadi
4. **Buyurtmalar tarixi** - Client ID bo'yicha tugallangan buyurtmalar PDF qilib yuboriladi
5. **ID tozalash** - `/clearid` komandasida ID o'chiriladi

## 🔧 Qo'shimcha komandalar

- `/start` - Botni boshlash va asosiy menyuga qaytish
- `/clearid` - Saqlangan Client ID ni o'chirish

## 🔒 Xavfsizlik

- `config.json` fayli `.gitignore` da saqlanadi
- Railway da environment variables ishlatiladi
- Google Service Account ma'lumotlari xavfsiz saqlanadi

## 📞 Yordam

Agar muammolar bo'lsa:
1. Railway logs ni tekshiring
2. Environment variables to'g'ri o'rnatilganini tekshiring
3. Google Sheets ruxsatlarini tekshiring

## ⚠️ Eslatma

- TRUE = Tayyor
- FALSE = Tayyorlanmoqda
- Bo'sh yuborilgan sana = "tez fursatda tayyor bo'ladi"
- Railway da webhook avtomatik o'rnatiladi
