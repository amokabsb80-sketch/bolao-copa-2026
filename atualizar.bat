@echo off
chcp 65001 >nul
cls

echo.
echo ╔══════════════════════════════════════════╗
echo ║     🏆 BOLÃO COPA 2026 - ATUALIZAR      ║
echo ╚══════════════════════════════════════════╝
echo.

echo 📋 Processando planilhas dos competidores...
.venv\Scripts\python.exe src/process_predictions.py

echo.
echo ╔══════════════════════════════════════════╗
echo ║            ✅ PRONTO!                    ║
echo ╚══════════════════════════════════════════╝
echo.
echo 🚀 Para iniciar o dashboard:
echo    Execute: iniciar_dashboard.bat
echo.

pause