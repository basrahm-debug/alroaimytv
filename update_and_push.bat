@echo off
REM ---------------------------------------------
REM 1. الذهاب إلى مجلد المشروع
cd /d E:\alroaimytv\alroaimytv

REM ---------------------------------------------
REM 2. تفعيل البيئة الافتراضية (إن وجدت)
IF EXIST venv (
    echo Activating virtual environment...
    call venv\Scripts\activate
)

REM ---------------------------------------------
REM 3. تثبيت مكتبات المشروع
echo Installing requirements...
pip install -r requirements.txt

REM ---------------------------------------------
REM 4. تشغيل سكربت تحديث القنوات
echo Updating channels.json...
python scripts\update_channels.py

REM ---------------------------------------------
REM 5. إضافة الملف إلى Git
echo Adding channels.json to git...
git add remote\channels.json

REM ---------------------------------------------
REM 6. عمل Commit
git commit -m "Auto update channels"

REM ---------------------------------------------
REM 7. Push إلى GitHub
git push

REM ---------------------------------------------
echo Done! Press any key to exit.
pause
