@echo off
SETLOCAL

chcp 65001

echo ------------------------------
echo تشغيل Ultimate IPTV Project
echo ------------------------------

REM تفعيل البيئة الافتراضية
IF NOT EXIST ".venv\Scripts\activate.bat" (
    echo انشاء البيئة الافتراضية...
    python -m venv .venv
)
call .venv\Scripts\activate.bat

REM تثبيت المكتبات المطلوبة
echo تثبيت المكتبات المطلوبة...
pip install --upgrade pip
pip install -r requirements.txt

REM تحديث القنوات
echo تحديث القنوات من M3U + YouTube...
python scripts/update_channels.py

REM رفع التحديثات إلى GitHub
echo رفع الملفات إلى GitHub...
git add .
git commit -m "Auto update channels and project files"
git push -u origin main

REM تشغيل واجهة الويب
echo تشغيل واجهة الويب...
cd "%~dp0\web_interface"
start "" python app.py

echo ------------------------------
echo العملية اكتملت!
pause
ENDLOCAL
