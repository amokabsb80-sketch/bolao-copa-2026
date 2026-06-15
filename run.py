#!/usr/bin/env python3
"""Menu principal do Bolão Copa 2026"""

import sys
import subprocess
from pathlib import Path

def limpar_tela():
    """Limpa a tela do terminal"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_banner():
    """Exibe banner do sistema"""
    print("\n" + "="*50)
    print("         🏆 BOLÃO COPA DO MUNDO 2026")
    print("="*50)
    print("   48 Seleções | 12 Grupos | 104 Jogos")
    print("   Canadá 🇨🇦 | México 🇲🇽 | EUA 🇺🇸")
    print("="*50)

def menu_principal():
    """Menu principal do sistema"""

    limpar_tela()
    mostrar_banner()

    print("\n📋 MENU PRINCIPAL:")
    print("  1. 📥 Baixar bandeiras das seleções")
    print("  2. 📋 Criar template para competidores")
    print("  3. ✅ Validar planilhas dos competidores")
    print("  4. 🖥️  Iniciar Dashboard")
    print("  5. 📊 Verificar status do sistema")
    print("  0. ❌ Sair")
    print("\n" + "-"*50)

    opcao = input("👉 Escolha uma opção: ").strip()

    if opcao == "1":
        print("\n📥 Baixando bandeiras das 48 seleções...")
        print("Isso pode levar alguns minutos...\n")
        subprocess.run([sys.executable, "utils/download_flags.py"])
        input("\nPressione Enter para continuar...")
        menu_principal()

    elif opcao == "2":
        print("\n📋 Criando template para competidores...\n")
        subprocess.run([sys.executable, "utils/create_template.py"])
        print("\n📝 O template foi salvo em: planilhas_competidores/")
        print("💡 Distribua para os 5 competidores preencherem!")
        input("\nPressione Enter para continuar...")
        menu_principal()

    elif opcao == "3":
        print("\n✅ Validando planilhas...\n")
        subprocess.run([sys.executable, "utils/validate_data.py"])
        input("\nPressione Enter para continuar...")
        menu_principal()

    elif opcao == "4":
        print("\n🖥️  Iniciando Dashboard...")
        print("📱 Acesse no navegador: http://localhost:8501")
        print("⚠️  Pressione Ctrl+C para parar o servidor\n")
        subprocess.run(["streamlit", "run", "src/dashboard.py"])
        menu_principal()

    elif opcao == "5":
        verificar_sistema()
        input("\nPressione Enter para continuar...")
        menu_principal()

    elif opcao == "0":
        print("\n👋 Até logo! Bom bolão! 🏆\n")
        sys.exit(0)

    else:
        print("\n❌ Opção inválida! Tente novamente.")
        input("\nPressione Enter para continuar...")
        menu_principal()

def verificar_sistema():
    """Verifica se tudo está configurado corretamente"""

    print("\n📊 VERIFICAÇÃO DO SISTEMA")
    print("="*50)

    # Verifica diretórios
    diretorios = [
        "assets/flags",
        "assets/avatars", 
        "planilhas_competidores",
        "data",
        "src",
        "utils"
    ]

    print("\n📁 Diretórios:")
    for d in diretorios:
        existe = Path(d).exists()
        status = "✅" if existe else "❌"
        print(f"   {status} {d}")

    # Verifica arquivos Python
    arquivos_py = [
        "src/copa2026_data.py",
        "src/assets_manager.py",
        "src/process_predictions.py",
        "src/manual_results.py",
        "src/scoring_engine.py",
        "src/dashboard.py"
    ]

    print("\n📄 Arquivos do sistema:")
    for a in arquivos_py:
        existe = Path(a).exists()
        status = "✅" if existe else "❌ (pendente)"
        print(f"   {status} {a}")

    # Verifica planilhas
    planilhas_dir = Path("planilhas_competidores")
    if planilhas_dir.exists():
        planilhas = list(planilhas_dir.glob("*.xlsx"))
        print(f"\n📋 Planilhas de competidores: {len(planilhas)}")
        for p in planilhas:
            if "TEMPLATE" in p.name.upper():
                print(f"   📋 {p.name} (template)")
            else:
                print(f"   📄 {p.name}")

    # Verifica bandeiras
    flags_dir = Path("assets/flags")
    if flags_dir.exists():
        bandeiras = list(flags_dir.glob("*.png"))
        print(f"\n🏳️  Bandeiras baixadas: {len(bandeiras)}/48")

        if len(bandeiras) < 48:
            print("   ⚠️  Execute a opção 1 para baixar todas as bandeiras")

    # Verifica dependências
    print("\n📦 Dependências:")
    try:
        import streamlit
        print("   ✅ Streamlit")
    except ImportError:
        print("   ❌ Streamlit (pip install streamlit)")

    try:
        import pandas
        print("   ✅ Pandas")
    except ImportError:
        print("   ❌ Pandas (pip install pandas)")

    try:
        import plotly
        print("   ✅ Plotly")
    except ImportError:
        print("   ❌ Plotly (pip install plotly)")

    try:
        import PIL
        print("   ✅ Pillow")
    except ImportError:
        print("   ❌ Pillow (pip install Pillow)")

if __name__ == "__main__":
    menu_principal()
