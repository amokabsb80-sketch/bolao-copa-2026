# utils/download_flags.py
print("Arquivo criado!")
# utils/download_flags.py
import requests
from pathlib import Path
import sys

# Adiciona src ao path
sys.path.append(str(Path(__file__).parent.parent))


def baixar_bandeiras():
    """Baixa bandeiras de todas as seleções"""

    # Mapeamento país -> código
    bandeiras = {
        # Grupo A
        'México': 'mx', 'África do Sul': 'za', 'Coreia do Sul': 'kr', 'República Tcheca': 'cz',
        # Grupo B
        'Canadá': 'ca', 'Bósnia-Herzegovina': 'ba', 'Catar': 'qa', 'Suíça': 'ch',
        # Grupo C
        'Brasil': 'br', 'Marrocos': 'ma', 'Haiti': 'ht', 'Escócia': 'gb-sct',
        # Grupo D
        'Estados Unidos': 'us', 'Paraguai': 'py', 'Austrália': 'au', 'Turquia': 'tr',
        # Grupo E
        'Alemanha': 'de', 'Curaçao': 'cw', 'Costa do Marfim': 'ci', 'Equador': 'ec',
        # Grupo F
        'Holanda': 'nl', 'Japão': 'jp', 'Suécia': 'se', 'Tunísia': 'tn',
        # Grupo G
        'Bélgica': 'be', 'Egito': 'eg', 'Irã': 'ir', 'Nova Zelândia': 'nz',
        # Grupo H
        'Espanha': 'es', 'Cabo Verde': 'cv', 'Arábia Saudita': 'sa', 'Uruguai': 'uy',
        # Grupo I
        'França': 'fr', 'Senegal': 'sn', 'Iraque': 'iq', 'Noruega': 'no',
        # Grupo J
        'Argentina': 'ar', 'Argélia': 'dz', 'Áustria': 'at', 'Jordânia': 'jo',
        # Grupo K
        'Portugal': 'pt', 'RD Congo': 'cd', 'Uzbequistão': 'uz', 'Colômbia': 'co',
        # Grupo L
        'Inglaterra': 'gb-eng', 'Croácia': 'hr', 'Gana': 'gh', 'Panamá': 'pa',
    }

    flags_dir = Path("assets/flags")
    flags_dir.mkdir(parents=True, exist_ok=True)

    total = len(bandeiras)
    sucesso = 0
    falha = 0

    print(f"\n🌍 Baixando {total} bandeiras...")
    print("=" * 50)

    for i, (pais, codigo) in enumerate(bandeiras.items(), 1):
        # URL da bandeira
        url = f"https://flagcdn.com/w160/{codigo}.png"

        # Nome do arquivo
        nome_arquivo = pais.lower()
        nome_arquivo = nome_arquivo.replace(' ', '_')
        nome_arquivo = nome_arquivo.replace('á', 'a').replace('é', 'e')
        nome_arquivo = nome_arquivo.replace('í', 'i').replace('ó', 'o')
        nome_arquivo = nome_arquivo.replace('ú', 'u').replace('ã', 'a')
        nome_arquivo = nome_arquivo.replace('õ', 'o').replace('ç', 'c')
        nome_arquivo = nome_arquivo.replace('ô', 'o').replace('ê', 'e')

        arquivo = flags_dir / f"{nome_arquivo}.png"

        try:
            print(f"[{i:2d}/{total}] {pais:25s} ", end='')

            response = requests.get(url, timeout=15)

            if response.status_code == 200:
                with open(arquivo, 'wb') as f:
                    f.write(response.content)
                print("✅")
                sucesso += 1
            else:
                # Tenta URL alternativa
                url_alt = f"https://flagcdn.com/80x60/{codigo}.png"
                response = requests.get(url_alt, timeout=15)

                if response.status_code == 200:
                    with open(arquivo, 'wb') as f:
                        f.write(response.content)
                    print("✅ (alt)")
                    sucesso += 1
                else:
                    print(f"❌ ({response.status_code})")
                    falha += 1

        except Exception as e:
            print(f"❌ Erro")
            falha += 1

    print("=" * 50)
    print(f"\n✅ Sucesso: {sucesso}/{total}")
    print(f"❌ Falhas:  {falha}/{total}")
    print(f"\n📁 Bandeiras salvas em: {flags_dir.absolute()}")


if __name__ == "__main__":
    baixar_bandeiras()