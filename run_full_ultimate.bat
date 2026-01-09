@echo off
SETLOCAL
chcp 65001

echo ------------------------------
echo تشغيل Ultimate IPTV Project
echo ------------------------------

REM 1️⃣ النسخ الاحتياطي لقنوات JSON
if exist "remote\channels.json" (
    echo اخذ نسخة احتياطية من channels.json...
    copy "remote\channels.json" "remote\channels_backup_%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%.json" >nul
)

REM 2️⃣ تفعيل أو إنشاء البيئة الافتراضية
IF NOT EXIST ".venv\Scripts\activate.bat" (
    echo انشاء البيئة الافتراضية...
    python -m venv .venv
)
call .venv\Scripts\activate.bat

REM 3️⃣ تثبيت المكتبات المطلوبة
if exist "requirements.txt" (
    echo تثبيت المكتبات المطلوبة...
    pip install --upgrade pip
    pip install -r requirements.txt
) else (
    echo WARNING: ملف requirements.txt غير موجود، سيتم تثبيت المكتبات يدويًا...
    pip install requests flet Flask yt-dlp jinja2
)

REM 4️⃣ تحديث القنوات تلقائيًا
echo تحديث القنوات من M3U + YouTube...
python scripts/update_channels.py

REM 5️⃣ رفع التحديثات إلى GitHub
echo رفع الملفات إلى GitHub...
git add .
git commit -m "Auto update channels and project files"
git pull --rebase origin main
git push -u origin main

REM 6️⃣ تشغيل واجهة الويب
echo تشغيل واجهة الويب...
cd "%~dp0\web_interface"
start "" python app.py

echo ------------------------------
echo العملية اكتملت بنجاح!
pause
ENDLOCAL
