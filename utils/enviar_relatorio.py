# utils/enviar_relatorio.py
"""Envia relatório do bolão para WhatsApp - Versão corrigida"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
from datetime import datetime
import json


def gerar_relatorio():
    """Gera o texto do relatório SEMPRE com dados atualizados"""

    # Força recarregar dados do JSON (sem cache)
    results_file = Path(__file__).parent.parent / "data" / "resultados_oficiais.json"
    print(f"📂 Procurando arquivo: {results_file}")
    print(f"📂 Existe: {results_file.exists()}")

    if not results_file.exists():
        return "⚠️ Nenhum resultado cadastrado ainda."

    with open(results_file, 'r', encoding='utf-8') as f:
        resultados = json.load(f)

    # Carrega previsões do CSV
    previsoes_file = Path("data/previsoes_consolidadas.csv")
    if previsoes_file.exists():
        predictions = pd.read_csv(previsoes_file)
    else:
        return "⚠️ Execute primeiro: python src/process_predictions.py"

    # Filtra apenas jogos realizados
    realizados = {}
    for match_id, dados in resultados.items():
        if dados.get('status') == 'Realizado' and dados.get('placar_casa') is not None:
            realizados[match_id] = dados

    if not realizados:
        return "⚠️ Nenhum jogo com resultado cadastrado."

    hoje = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Monta relatório
    relatorio = f"""
🏆 *BOLÃO COPA 2026 - RELATÓRIO*
📅 {hoje}

━━━━━━━━━━━━━━━━━━

📊 *RANKING ATUAL*

"""

    # Calcula ranking manualmente
    ranking = {}
    for match_id, jogo in realizados.items():
        casa = jogo.get('casa', '')
        visitante = jogo.get('visitante', '')
        placar_casa = jogo.get('placar_casa', 0)
        placar_visitante = jogo.get('placar_visitante', 0)

        # Busca palpites para este jogo
        palpites = predictions[
            (predictions['time_casa'] == casa) &
            (predictions['time_visitante'] == visitante)
            ]

        for _, palpite in palpites.iterrows():
            competidor = palpite['competidor']
            pred_casa = int(palpite['placar_casa_previsto']) if pd.notna(palpite.get('placar_casa_previsto')) else -1
            pred_visit = int(palpite['placar_visitante_previsto']) if pd.notna(
                palpite.get('placar_visitante_previsto')) else -1

            if pred_casa == -1:
                continue

            # Calcula pontos
            if pred_casa == placar_casa and pred_visit == placar_visitante:
                pontos = 35
            elif (pred_casa > pred_visit and placar_casa > placar_visitante) or \
                    (pred_casa < pred_visit and placar_casa < placar_visitante) or \
                    (pred_casa == pred_visit and placar_casa == placar_visitante):
                pontos = 15
            else:
                pontos = 0

            if competidor not in ranking:
                ranking[competidor] = {'pontos': 0, 'placares': 0, 'resultados': 0}

            ranking[competidor]['pontos'] += pontos
            if pontos == 35:
                ranking[competidor]['placares'] += 1
            elif pontos == 15:
                ranking[competidor]['resultados'] += 1

    # Ordena ranking
    ranking_ordenado = sorted(ranking.items(), key=lambda x: x[1]['pontos'], reverse=True)

    medals = {0: '🥇', 1: '🥈', 2: '🥉', 3: '4º', 4: '5º'}
    for i, (nome, dados) in enumerate(ranking_ordenado[:5]):
        medal = medals.get(i, f'{i + 1}º')
        relatorio += f"{medal} *{nome}* - {dados['pontos']} pts"
        if dados['placares'] > 0:
            relatorio += f" ({dados['placares']} 🎯)"
        relatorio += "\n"

    # Últimos 5 jogos (ordenados por data)
    relatorio += """
━━━━━━━━━━━━━━━━━━

⚽ *ÚLTIMOS JOGOS*

"""

    jogos_ordenados = sorted(realizados.items(),
                             key=lambda x: x[1].get('data', ''),
                             reverse=True)

    for match_id, jogo in jogos_ordenados[:5]:
        casa = jogo.get('casa', '')
        visitante = jogo.get('visitante', '')
        placar = f"{jogo.get('placar_casa', 0)} x {jogo.get('placar_visitante', 0)}"
        data = jogo.get('data', '')

        relatorio += f"\n⚽ *{casa}* {placar} *{visitante}* ({data})\n"

        # Palpites para este jogo
        palpites = predictions[
            (predictions['time_casa'] == casa) &
            (predictions['time_visitante'] == visitante)
            ]

        for _, palpite in palpites.iterrows():
            competidor = palpite['competidor']
            pred_casa = int(palpite['placar_casa_previsto']) if pd.notna(palpite.get('placar_casa_previsto')) else -1
            pred_visit = int(palpite['placar_visitante_previsto']) if pd.notna(
                palpite.get('placar_visitante_previsto')) else -1

            if pred_casa == -1:
                continue

            pred = f"{pred_casa} x {pred_visit}"

            # Calcula ícone
            if pred_casa == jogo.get('placar_casa') and pred_visit == jogo.get('placar_visitante'):
                icon = "🎯"
            elif (pred_casa > pred_visit and jogo.get('placar_casa') > jogo.get('placar_visitante')) or \
                    (pred_casa < pred_visit and jogo.get('placar_casa') < jogo.get('placar_visitante')) or \
                    (pred_casa == pred_visit and jogo.get('placar_casa') == jogo.get('placar_visitante')):
                icon = "✓"
            else:
                icon = "✗"

            # Pontos
            if icon == "🎯":
                pts = 35
            elif icon == "✓":
                pts = 15
            else:
                pts = 0

            relatorio += f"  {icon} {competidor}: {pred} ({pts} pts)\n"

    relatorio += """
━━━━━━━━━━━━━━━━━━
📱 _Relatório automático do Bolão_
"""

    return relatorio


def enviar_whatsapp_contato(numero: str, mensagem: str):
    """Envia mensagem para um contato específico"""
    import pywhatkit as kit

    try:
        kit.sendwhatmsg_instantly(
            phone_no=numero,
            message=mensagem,
            wait_time=15,
            tab_close=True
        )
        print("✅ Relatório enviado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar: {e}")
        print("\n📋 Relatório gerado (envio manual):")
        print(mensagem)
        return False


# ============================================
# EXECUÇÃO
# ============================================
if __name__ == "__main__":
    print("\n📊 Gerando relatório...")

    relatorio = gerar_relatorio()
    print(relatorio)

    print("\n" + "=" * 50)
    print("Opções:")
    print("1. Enviar para WhatsApp")
    print("2. Salvar arquivo")
    print("3. Copiar texto")

    opcao = input("\nEscolha (1/2/3): ").strip()

    if opcao == "1":
        numero = input("Número (ex: +5511999998888): ").strip()
        enviar_whatsapp_contato(numero, relatorio)
    elif opcao == "2":
        arquivo = Path("data") / f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        arquivo.parent.mkdir(exist_ok=True)
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write(relatorio)
        print(f"💾 Salvo em: {arquivo}")
    elif opcao == "3":
        print("✅ Copie o texto acima e cole no WhatsApp")