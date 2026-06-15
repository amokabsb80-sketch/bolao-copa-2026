# utils/create_template.py
print("Arquivo criado!")
# utils/create_template.py
import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from src.copa2026_data import JOGOS_FASE_GRUPOS


def criar_template():
    """Cria planilha template para competidores"""

    dados = []
    for jogo in JOGOS_FASE_GRUPOS:
        dados.append({
            'GRUPO': jogo['grupo'],
            'RODADA': jogo['rodada'],
            'DATA': jogo['data'],
            'HORA': jogo['hora'],
            'TIME_CASA': jogo['casa'],
            'TIME_VISITANTE': jogo['visitante'],
            'CIDADE': jogo['cidade'],
            'PLACAR_CASA_PREVISTO': '',
            'PLACAR_VISITANTE_PREVISTO': '',
        })

    df = pd.DataFrame(dados)
    df['DATA'] = pd.to_datetime(df['DATA']).dt.strftime('%d/%m/%Y')

    # Salva
    pasta = Path("planilhas_competidores")
    pasta.mkdir(exist_ok=True)

    arquivo = pasta / "TEMPLATE_NOME_COMPETIDOR.xlsx"
    df.to_excel(arquivo, index=False)

    print(f"\n✅ Template criado: {arquivo}")
    print(f"📋 {len(dados)} jogos da fase de grupos")
    print("\n📝 INSTRUÇÕES:")
    print("1. Cada competidor deve RENOMEAR o arquivo")
    print("   Ex: JOAO_previsoes.xlsx")
    print("2. Preencher APENAS as colunas:")
    print("   - PLACAR_CASA_PREVISTO")
    print("   - PLACAR_VISITANTE_PREVISTO")
    print("3. Usar apenas números inteiros (0, 1, 2, etc)")
    print("4. NÃO alterar a ordem das linhas!")


if __name__ == "__main__":
    criar_template()