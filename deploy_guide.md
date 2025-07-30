# NEMAT LASER SERVICE Bot - Deployment Qo'llanmasi

## 🚀 GitHub va Railway ga Deployment

### 1. GitHub Repository Yaratish

#### 1.1 GitHub da yangi repository yarating
1. [GitHub.com](https://github.com) ga o'ting
2. "New repository" tugmasini bosing
3. Repository nomini kiriting: `nls-bot`
4. "Public" ni tanlang
5. "Create repository" tugmasini bosing

#### 1.2 Local kompyuteringizda Git repository yarating
```bash
# Loyiha papkasiga o'ting
cd /path/to/NLS_bot

# Git repository yarating
git init

# Barcha fayllarni qo'shing
git add .

# Birinchi commit yarating
git commit -m "Initial commit: NEMAT LASER SERVICE Bot"

# GitHub repository ga ulang
git remote add origin https://github.com/YOUR_USERNAME/nls-bot.git

# Main branch ni o'rnating
git branch -M main

# GitHub ga push qiling
git push -u origin main
```

### 2. Railway Deployment

#### 2.1 Railway ga kirish
1. [Railway.app](https://railway.app) ga o'ting
2. GitHub account bilan tizimga kiring
3. "Start a New Project" tugmasini bosing

#### 2.2 GitHub Repository ni ulash
1. "Deploy from GitHub repo" ni tanlang
2. GitHub repositoryingizni tanlang (`nls-bot`)
3. "Deploy Now" tugmasini bosing

#### 2.3 Environment Variables o'rnatish

Railway project da "Variables" bo'limiga o'ting va quyidagi o'zgaruvchilarni qo'shing:

**TELEGRAM_BOT_TOKEN**
```
8217986861:AAHt1wKH8psE-5nuZJUNbJcwUxBSx8pSjvw
```

**GOOGLE_SHEETS_ID**
```
1PwXbGkPGR8_EHE9sIPZcE3vW7wLWEH-CHViBjvMp_fA
```

**GOOGLE_CREDENTIALS**
```
{"type":"service_account","project_id":"your-project-id","private_key_id":"your-private-key-id","private_key":"-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n","client_email":"your-service-account@your-project.iam.gserviceaccount.com","client_id":"your-client-id","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"}
```

**ORDERS_SHEET**
```
List1
```

**USERS_SHEET**
```
List3
```

### 3. Google Service Account Sozlash

#### 3.1 Google Cloud Console ga kirish
1. [Google Cloud Console](https://console.cloud.google.com/) ga o'ting
2. Yangi project yarating yoki mavjud project ni tanlang

#### 3.2 Google Sheets API ni yoqish
1. "APIs & Services" > "Library" ga o'ting
2. "Google Sheets API" ni qidiring va yoqing
3. "Google Drive API" ni ham yoqing

#### 3.3 Service Account yarating
1. "APIs & Services" > "Credentials" ga o'ting
2. "Create Credentials" > "Service Account" ni tanlang
3. Service Account nomini kiriting: `nls-bot-service`
4. "Create and Continue" tugmasini bosing
5. "Role" ni "Editor" ga o'rnating
6. "Done" tugmasini bosing

#### 3.4 JSON Key yarating
1. Service Account ro'yxatida yangi yaratilgan account ni bosing
2. "Keys" bo'limiga o'ting
3. "Add Key" > "Create new key" ni tanlang
4. "JSON" formatini tanlang
5. "Create" tugmasini bosing
6. JSON fayl yuklab olinadi

#### 3.5 JSON ma'lumotlarini Railway ga qo'shish
1. Yuklab olingan JSON faylini oching
2. Barcha ma'lumotlarni nusxalang
3. Railway da `GOOGLE_CREDENTIALS` o'zgaruvchisiga yopishtiring

#### 3.6 Google Sheets ga ruxsat bering
1. Google Sheets faylingizni oching
2. "Share" tugmasini bosing
3. Service Account email manzilini qo'shing
4. "Editor" ruxsatini bering

### 4. Telegram Bot Webhook Sozlash

#### 4.1 Railway URL ni olish
1. Railway project da "Settings" ga o'ting
2. "Domains" bo'limida URL ni ko'ring
3. URL shakli: `https://your-app-name.railway.app`

#### 4.2 Webhook o'rnatish
Terminal da quyidagi komandani ishga tushiring:

```bash
curl -X POST "https://api.telegram.org/bot8217986861:AAHt1wKH8psE-5nuZJUNbJcwUxBSx8pSjvw/setWebhook" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://your-app-name.railway.app/webhook"}'
```

**Eslatma:** `your-app-name` ni Railway da berilgan haqiqiy app nomi bilan almashtiring.

### 5. Deployment Tekshirish

#### 5.1 Railway Logs ni tekshirish
1. Railway project da "Deployments" bo'limiga o'ting
2. Eng so'nggi deployment ni bosing
3. "View Logs" tugmasini bosing
4. Xatoliklar bor-yo'qligini tekshiring

#### 5.2 Bot ishlashini tekshirish
1. Telegram da botingizga o'ting
2. `/start` komandasi yuboring
3. Bot javob berishini tekshiring

### 6. Muammolar va Yechimlar

#### 6.1 Bot javob bermaydi
- Railway logs ni tekshiring
- Environment variables to'g'ri o'rnatilganini tekshiring
- Webhook URL to'g'ri o'rnatilganini tekshiring

#### 6.2 Google Sheets bilan bog'lanishda xatolik
- `GOOGLE_CREDENTIALS` to'g'ri formatda ekanligini tekshiring
- Google Sheets ga ruxsat berilganini tekshiring
- Google Sheets API yoqilganini tekshiring

#### 6.3 PDF fayllar yaratilmaydi
- Railway da fayl yaratish ruxsati borligini tekshiring
- `fpdf2` kutubxonasi o'rnatilganini tekshiring

### 7. Yangilanishlar

Kodni yangilash uchun:
```bash
# O'zgarishlarni qo'shing
git add .
git commit -m "Update: yangi xususiyatlar"
git push origin main
```

Railway avtomatik ravishda yangi deployment qiladi.

### 8. Monitoring

#### 8.1 Railway Monitoring
- Railway dashboard da "Metrics" bo'limini tekshiring
- CPU va Memory ishlatilishini kuzating

#### 8.2 Bot Monitoring
- Telegram da bot ishlashini muntazam tekshiring
- Foydalanuvchilar xabar yuborishini kuzating

## ✅ Deployment Tugagandan So'ng

1. ✅ GitHub repository yaratildi
2. ✅ Railway project yaratildi
3. ✅ Environment variables o'rnatildi
4. ✅ Google Service Account sozlandi
5. ✅ Webhook o'rnatildi
6. ✅ Bot ishlayapti

Endi sizning NEMAT LASER SERVICE botingiz to'liq professional darajada ishlayapti! 🎉 