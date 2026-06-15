@echo off
chcp 65001 >nul
cls

echo.
echo ╔══════════════════════════════════════════╗
echo ║  📤 ATUALIZAR DADOS E SUBIR PARA GIT    ║
echo ╚══════════════════════════════════════════╝
echo.

echo 📋 Processando planilhas...
.venv\Scripts\python.exe src/process_predictions.py

echo.
echo 📤 Subindo para o GitHub...
git add data/resultados_oficiais.json
git add data/previsoes_consolidadas.csv
git add data/pontuacao_completa.csv
git commit -m "Atualizando resultados %date% %time%"
git push

echo.
echo ✅ Dados atualizados no GitHub!
echo 🔄 O Streamlit Cloud vai atualizar automaticamente.
echo.

pause