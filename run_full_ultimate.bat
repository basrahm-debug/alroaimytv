@echo off
REM ====================================================
REM IPTV Ultimate Automation: Update + YouTube + Git + Web UI
REM ====================================================

REM 1️⃣ الانتقال إلى مجلد المشروع
cd /d E:\alroaimytv\alroaimytv

REM ====================================================
REM 2️⃣ تفعيل البيئة الافتراضية (إذا موجودة)
IF EXIST venv (
    echo Activating virtual environment...
    call venv\Scripts\activate
)

REM ====================================================
REM 3️⃣ تثبيت المكتبات المطلوبة
echo Installing required Python packages...
pip install -r requirements.txt
pip install yt-dlp --upgrade

REM ====================================================
REM 4️⃣ تحديث القنوات تلقائيًا (M3U + Direct + YouTube)
echo Updating channels.json...
python scripts\update_channels.py

REM ====================================================
REM 5️⃣ عرض عدد القنوات بعد التحديث
python - <<END
import json
with open("remote/channels.json","r",encoding="utf-8") as f:
    data=json.load(f)
count=sum(len(cat.get("channels",[])) for cat in data.get("categories",[]))
print(f"تم تحديث {count} قناة في المجموع.")
END

REM ====================================================
REM 6️⃣ Git: إضافة الملفات المهمة فقط
git add -u remote/channels.json
git add update_and_push.bat

REM ====================================================
REM 7️⃣ Commit & Push إلى GitHub
git commit -m "Auto-update channels including YouTube"
git push

REM ====================================================
REM 8️⃣ فتح المتصفح تلقائيًا على الواجهة المتقدمة
echo Launching advanced web interface...
start "" python -m webbrowser -t "http://127.0.0.1:5000/"

REM ====================================================
REM 9️⃣ تشغيل Flask في نافذة جديدة
start "" cmd /k python web_interface\app.py

REM ====================================================
echo ==========================================
echo كل شيء جاهز! الواجهة المتقدمة مفتوحة الآن.
echo اضغط أي مفتاح للإغلاق.
pause
