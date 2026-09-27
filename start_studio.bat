@echo off
title VisionCraft DIP Studio Launcher
echo ================================================================
echo    Starting VisionCraft DIP Studio (Python Engine + Laravel)
echo ================================================================
echo.

:: 1. تشغيل محرك بايثون في نافذة منفصلة
echo [1/3] Starting Python DIP Engine (Port 5001)...
start "VisionCraft Python Engine" cmd /k "python python_engine/run.py"

:: 2. تشغيل سيرفر لارافل في نافذة منفصلة
echo [2/3] Starting Laravel Server (Port 8000)...
start "VisionCraft Laravel Server" cmd /k "php artisan serve"

:: 3. الانتظار ثانيتين ثم فتح المتصفح تلقائياً
echo [3/3] Opening Studio in browser...
timeout /t 3 /nobreak >nul
start http://127.0.0.1:8000

echo.
echo ================================================================
echo    VisionCraft Studio is now running at: http://127.0.0.1:8000
echo ================================================================
