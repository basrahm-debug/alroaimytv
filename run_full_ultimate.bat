@echo off
SETLOCAL

echo ------------------------------
echo تشغيل Ultimate IPTV Project
echo ------------------------------

REM 1️⃣ تفعيل أو إنشاء البيئة الافتراضية
IF NOT EXIST ".venv\Scripts\activate.bat" (
    echo انشاء البيئة الافتراضية...
    python -m venv .venv
)
echo تفعيل البيئة الافتراضية...
call .venv\Scripts\activate.bat

REM 2️⃣ تثبيت المتطلبات
echo تثبيت المكتبات المطلوبة...
pip install --upgrade pip
pip install -r requirements.txt

REM 3️⃣ تحديث القنوات تلقائيًا
echo تحديث القنوات من M3U + YouTube...
python scripts/update_channels.py

REM 4️⃣ رفع التحديثات إلى GitHub
echo رفع الملفات إلى GitHub...
git add .
git commit -m "Auto update channels and project files"
git push -u origin main

REM 5️⃣ تشغيل واجهة الويب
echo تشغيل واجهة الويب...
cd web_interface
start "" python app.py

echo ------------------------------
echo العملية اكتملت!
pause
ENDLOCAL
