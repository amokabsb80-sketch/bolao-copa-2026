@echo off
chcp 65001 >nul
cls

echo.
echo ╔══════════════════════════════════════════╗
echo ║   📊 ENVIAR RELATÓRIO DO BOLÃO          ║
echo ╚══════════════════════════════════════════╝
echo.
echo ⚠️  IMPORTANTE:
echo    - WhatsApp Web deve estar logado no navegador
echo    - Não mexa no mouse durante o envio
echo.

.venv\Scripts\python.exe utils/enviar_relatorio.py

pause