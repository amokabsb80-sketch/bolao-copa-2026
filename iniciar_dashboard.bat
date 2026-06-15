@echo off
chcp 65001 >nul
cls

echo.
echo ╔══════════════════════════════════════════╗
echo ║   🏆 INICIANDO DASHBOARD COPA 2026      ║
echo ╚══════════════════════════════════════════╝
echo.

echo 🚀 Iniciando servidor...
echo.
echo 📱 Acesse: http://localhost:8501
echo ⚠️  Pressione Ctrl+C para parar
echo.

.venv\Scripts\python.exe -m streamlit run src/dashboard.py

pause