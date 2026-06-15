# setup.py - Execute este arquivo PRIMEIRO para criar toda a estrutura
"""
Script de configuração inicial do Bolão Copa 2026
Cria toda a estrutura de diretórios e arquivos necessários
Execute: python setup.py
"""

import os
import sys
import json
from pathlib import Path


def criar_estrutura_projeto():
    """Cria toda a estrutura de diretórios do projeto"""

    print("\n" + "=" * 60)
    print("🏆 CONFIGURANDO BOLÃO COPA DO MUNDO 2026")
    print("=" * 60)

    # Diretório raiz do projeto (usa o diretório atual)
    raiz = Path.cwd()

    # Estrutura de diretórios
    diretorios = [
        "assets/flags",
        "assets/avatars",
        "planilhas_competidores",
        "data",
        "src",
        "utils",
    ]

    print("\n📁 Criando diretórios...")
    for dir_path in diretorios:
        caminho_completo = raiz / dir_path
        caminho_completo.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {dir_path}")

    print(f"\n✅ Estrutura criada com sucesso!")
    return raiz


def criar_requirements(raiz: Path):
    """Cria arquivo requirements.txt"""

    conteudo = [
        "# Bolão Copa 2026 - Dependências",
        "streamlit==1.32.0",
        "pandas==2.2.0",
        "plotly==5.18.0",
        "openpyxl==3.1.2",
        "requests==2.31.0",
        "Pillow==10.2.0",
        "numpy==1.26.3",
        "python-dateutil==2.8.2",
        ""
    ]

    with open(raiz / "requirements.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(conteudo))
    print("   ✅ requirements.txt")


def criar_gitignore(raiz: Path):
    """Cria arquivo .gitignore"""

    conteudo = [
        "# Python",
        "__pycache__/",
        "*.py[cod]",
        "*.so",
        "*.egg-info/",
        "dist/",
        "build/",
        ".env",
        "venv/",
        "env/",
        "",
        "# Streamlit",
        ".streamlit/secrets.toml",
        "",
        "# Dados",
        "data/*.csv",
        "data/*.json",
        "*.xlsx",
        "!planilhas_competidores/TEMPLATE_*.xlsx",
        "",
        "# Assets",
        "assets/flags/*.png",
        "assets/avatars/*.png",
        "",
        "# IDE",
        ".vscode/",
        ".idea/",
        "*.swp",
        "*.swo",
        ""
    ]

    with open(raiz / ".gitignore", "w", encoding="utf-8") as f:
        f.write("\n".join(conteudo))
    print("   ✅ .gitignore")


def criar_readme(raiz: Path):
    """Cria arquivo README.md"""

    conteudo = [
        "# 🏆 Bolão Copa do Mundo 2026",
        "",
        "Sistema completo para gerenciar bolão da Copa do Mundo FIFA 2026",
        "- **48 seleções** | **12 grupos** (A-L) | **72 jogos** na fase de grupos",
        "- Sedes: Canadá, México e Estados Unidos",
        "- Data: 11 de junho a 19 de julho de 2026",
        "",
        "## 📋 Regras de Pontuação",
        "- Acertou o resultado do jogo (vitória/empate/derrota): **15 pontos**",
        "- Acertou o placar exato: **30 pontos**",
        "",
        "## 🚀 Instalação e Uso",
        "",
        "### 1. Instalar dependências",
        "```bash",
        "pip install -r requirements.txt",
        "```",
        "",
        "### 2. Baixar bandeiras das seleções",
        "```bash",
        "python utils/download_flags.py",
        "```",
        "",
        "### 3. Criar template para competidores",
        "```bash",
        "python utils/create_template.py",
        "```",
        "",
        "### 4. Coletar palpites",
        "Distribua o template gerado em `planilhas_competidores/` para cada competidor.",
        "Cada um deve salvar como: `NOME_previsoes.xlsx`",
        "",
        "### 5. Validar planilhas (opcional)",
        "```bash",
        "python utils/validate_data.py",
        "```",
        "",
        "### 6. Executar o dashboard",
        "```bash",
        "streamlit run src/dashboard.py",
        "```",
        "Acesse no navegador: http://localhost:8501",
        "",
        "### 7. Menu rápido",
        "```bash",
        "python run.py",
        "```",
        "",
        "## 📁 Estrutura do Projeto",
        "```",
        "bolao-copa-2026/",
        "├── assets/                    # Bandeiras e avatares",
        "├── planilhas_competidores/    # Planilhas de palpites",
        "├── data/                      # Dados processados",
        "├── src/                       # Código fonte",
        "├── utils/                     # Utilitários",
        "├── requirements.txt          # Dependências",
        "└── run.py                    # Menu principal",
        "```",
        "",
        "## 🎯 Funcionalidades",
        "- Dashboard interativo com Streamlit",
        "- Bandeiras oficiais de todas as 48 seleções",
        "- Avatares personalizados para competidores",
        "- Atualização manual de resultados",
        "- Cálculo automático de pontuação",
        "- Ranking em tempo real",
        "- Gráficos e estatísticas",
        "",
        "## 📊 Tecnologias",
        "- Python 3.10+",
        "- Streamlit (Dashboard)",
        "- Pandas (Processamento de dados)",
        "- Plotly (Gráficos)",
        "- Pillow (Imagens)",
        ""
    ]

    with open(raiz / "README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(conteudo))
    print("   ✅ README.md")


def criar_init_src(raiz: Path):
    """Cria __init__.py do pacote src"""

    with open(raiz / "src" / "__init__.py", "w", encoding="utf-8") as f:
        f.write('"""Pacote principal do Bolão Copa 2026"""\n')
        f.write('__version__ = "1.0.0"\n')
    print("   ✅ src/__init__.py")


def criar_competitors_json(raiz: Path):
    """Cria arquivo de configuração dos competidores"""

    config = {
        "competidores": {
            "competidor_1": {
                "nome": "Competidor 1",
                "apelido": "Comp1",
                "cor": "#FF6B6B",
                "emoji": "⚽",
                "ativo": True
            },
            "competidor_2": {
                "nome": "Competidor 2",
                "apelido": "Comp2",
                "cor": "#4ECDC4",
                "emoji": "🌟",
                "ativo": True
            },
            "competidor_3": {
                "nome": "Competidor 3",
                "apelido": "Comp3",
                "cor": "#45B7D1",
                "emoji": "🔥",
                "ativo": True
            },
            "competidor_4": {
                "nome": "Competidor 4",
                "apelido": "Comp4",
                "cor": "#96CEB4",
                "emoji": "💫",
                "ativo": True
            },
            "competidor_5": {
                "nome": "Competidor 5",
                "apelido": "Comp5",
                "cor": "#DDA0DD",
                "emoji": "🎯",
                "ativo": True
            }
        },
        "configuracoes_gerais": {
            "nome_bolao": "Bolão Copa 2026",
            "pontos_resultado": 15,
            "pontos_placar": 30,
            "data_inicio": "2026-06-11",
            "data_fim": "2026-07-19",
            "total_competidores": 5
        }
    }

    with open(raiz / "assets" / "competitors.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print("   ✅ assets/competitors.json")


def criar_run_py(raiz: Path):
    """Cria script run.py com menu principal"""

    codigo = '''#!/usr/bin/env python3
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
    print("\\n" + "="*50)
    print("         🏆 BOLÃO COPA DO MUNDO 2026")
    print("="*50)
    print("   48 Seleções | 12 Grupos | 104 Jogos")
    print("   Canadá 🇨🇦 | México 🇲🇽 | EUA 🇺🇸")
    print("="*50)

def menu_principal():
    """Menu principal do sistema"""

    limpar_tela()
    mostrar_banner()

    print("\\n📋 MENU PRINCIPAL:")
    print("  1. 📥 Baixar bandeiras das seleções")
    print("  2. 📋 Criar template para competidores")
    print("  3. ✅ Validar planilhas dos competidores")
    print("  4. 🖥️  Iniciar Dashboard")
    print("  5. 📊 Verificar status do sistema")
    print("  0. ❌ Sair")
    print("\\n" + "-"*50)

    opcao = input("👉 Escolha uma opção: ").strip()

    if opcao == "1":
        print("\\n📥 Baixando bandeiras das 48 seleções...")
        print("Isso pode levar alguns minutos...\\n")
        subprocess.run([sys.executable, "utils/download_flags.py"])
        input("\\nPressione Enter para continuar...")
        menu_principal()

    elif opcao == "2":
        print("\\n📋 Criando template para competidores...\\n")
        subprocess.run([sys.executable, "utils/create_template.py"])
        print("\\n📝 O template foi salvo em: planilhas_competidores/")
        print("💡 Distribua para os 5 competidores preencherem!")
        input("\\nPressione Enter para continuar...")
        menu_principal()

    elif opcao == "3":
        print("\\n✅ Validando planilhas...\\n")
        subprocess.run([sys.executable, "utils/validate_data.py"])
        input("\\nPressione Enter para continuar...")
        menu_principal()

    elif opcao == "4":
        print("\\n🖥️  Iniciando Dashboard...")
        print("📱 Acesse no navegador: http://localhost:8501")
        print("⚠️  Pressione Ctrl+C para parar o servidor\\n")
        subprocess.run(["streamlit", "run", "src/dashboard.py"])
        menu_principal()

    elif opcao == "5":
        verificar_sistema()
        input("\\nPressione Enter para continuar...")
        menu_principal()

    elif opcao == "0":
        print("\\n👋 Até logo! Bom bolão! 🏆\\n")
        sys.exit(0)

    else:
        print("\\n❌ Opção inválida! Tente novamente.")
        input("\\nPressione Enter para continuar...")
        menu_principal()

def verificar_sistema():
    """Verifica se tudo está configurado corretamente"""

    print("\\n📊 VERIFICAÇÃO DO SISTEMA")
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

    print("\\n📁 Diretórios:")
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

    print("\\n📄 Arquivos do sistema:")
    for a in arquivos_py:
        existe = Path(a).exists()
        status = "✅" if existe else "❌ (pendente)"
        print(f"   {status} {a}")

    # Verifica planilhas
    planilhas_dir = Path("planilhas_competidores")
    if planilhas_dir.exists():
        planilhas = list(planilhas_dir.glob("*.xlsx"))
        print(f"\\n📋 Planilhas de competidores: {len(planilhas)}")
        for p in planilhas:
            if "TEMPLATE" in p.name.upper():
                print(f"   📋 {p.name} (template)")
            else:
                print(f"   📄 {p.name}")

    # Verifica bandeiras
    flags_dir = Path("assets/flags")
    if flags_dir.exists():
        bandeiras = list(flags_dir.glob("*.png"))
        print(f"\\n🏳️  Bandeiras baixadas: {len(bandeiras)}/48")

        if len(bandeiras) < 48:
            print("   ⚠️  Execute a opção 1 para baixar todas as bandeiras")

    # Verifica dependências
    print("\\n📦 Dependências:")
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
'''

    with open(raiz / "run.py", "w", encoding="utf-8") as f:
        f.write(codigo)
    print("   ✅ run.py")


def criar_arquivos_vazios_src(raiz: Path):
    """Cria arquivos Python vazios no src para evitar erros de import"""

    arquivos = [
        "copa2026_data.py",
        "assets_manager.py",
        "process_predictions.py",
        "manual_results.py",
        "scoring_engine.py",
        "dashboard.py"
    ]

    for arquivo in arquivos:
        caminho = raiz / "src" / arquivo
        if not caminho.exists():
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(f'"""Módulo: {arquivo}"""\n')
                f.write('# Em desenvolvimento...\n')
    print("   ✅ Arquivos base criados em src/")


def main():
    """Função principal de setup"""

    print("\n" + "=" * 60)
    print("🚀 INICIANDO CONFIGURAÇÃO DO PROJETO")
    print("=" * 60)

    # 1. Cria estrutura de diretórios
    raiz = criar_estrutura_projeto()

    # 2. Cria arquivos de configuração
    print("\n📄 Criando arquivos de configuração...")
    criar_requirements(raiz)
    criar_gitignore(raiz)
    criar_readme(raiz)
    criar_init_src(raiz)
    criar_competitors_json(raiz)

    # 3. Cria arquivos Python base
    print("\n🐍 Criando arquivos Python base...")
    criar_arquivos_vazios_src(raiz)

    # 4. Cria script run.py
    print("\n🚀 Criando menu principal...")
    criar_run_py(raiz)

    # Resumo final
    print("\n" + "=" * 60)
    print("✅ CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 60)

    print(f"\n📁 Projeto criado em: {raiz.absolute()}")

    print("\n📝 PRÓXIMOS PASSOS:")
    print("  1. Instalar dependências:")
    print("     pip install -r requirements.txt")
    print()
    print("  2. Baixar bandeiras:")
    print("     python utils/download_flags.py")
    print()
    print("  3. Criar template para competidores:")
    print("     python utils/create_template.py")
    print()
    print("  4. Ou use o menu completo:")
    print("     python run.py")

    print("\n" + "=" * 60)
    print("🏆 BOM BOLÃO! QUE VENÇA O MELHOR!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()