# utils/enviar_relatorio.py
"""
Envia relatório do bolão para WhatsApp
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
from datetime import datetime
from src.process_predictions import PredictionProcessor
from src.manual_results import ManualResultsManager
from src.scoring_engine import ScoringEngine


def gerar_relatorio():
    """Gera o texto do relatório"""

    # Carrega dados
    processor = PredictionProcessor()
    results_manager = ManualResultsManager()
    engine = ScoringEngine()

    predictions = processor.consolidate_predictions()
    real_results = results_manager.get_only_completed_results()

    if predictions.empty or real_results.empty:
        return "⚠️ Dados insuficientes para gerar relatório."

    scored = engine.calculate_scores(predictions, real_results)
    leaderboard = engine.get_leaderboard(scored)

    # Data do relatório
    hoje = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Monta o relatório
    relatorio = f"""
🏆 *BOLÃO COPA 2026 - RELATÓRIO*
📅 {hoje}

━━━━━━━━━━━━━━━━━━

📊 *RANKING ATUAL*

"""

    # Top 5
    medals = {1: '🥇', 2: '🥈', 3: '🥉', 4: '4º', 5: '5º'}

    for _, row in leaderboard.head(5).iterrows():
        pos = int(row['posicao'])
        medal = medals.get(pos, f'{pos}º')
        pontos = int(row['pontos_total'])
        placares = int(row['placares_exatos'])

        relatorio += f"{medal} *{row['competidor']}* - {pontos} pts"
        if placares > 0:
            relatorio += f" ({placares} 🎯)"
        relatorio += "\n"

    relatorio += """
━━━━━━━━━━━━━━━━━━

⚽ *ÚLTIMOS JOGOS*

"""

    # Últimos 3 jogos com resultado
    ultimos_jogos = real_results.tail(3)

    for _, jogo in ultimos_jogos.iterrows():
        placar = f"{int(jogo['placar_casa'])} x {int(jogo['placar_visitante'])}"

        # Busca palpites para este jogo
        palpites_jogo = scored[
            (scored['time_casa'] == jogo['time_casa']) &
            (scored['time_visitante'] == jogo['time_visitante'])
            ]

        relatorio += f"\n⚽ *{jogo['time_casa']}* {placar} *{jogo['time_visitante']}*\n"

        for _, palpite in palpites_jogo.iterrows():
            pts = int(palpite['pontos'])
            # Palpite do competidor
            prev_casa = int(palpite['placar_casa_previsto'])
            prev_visitante = int(palpite['placar_visitante_previsto'])

            if palpite['acertou_placar']:
                icon = "🎯"
            elif palpite['acertou_resultado']:
                icon = "✓"
            else:
                icon = "✗"

            relatorio += f"  {icon} {palpite['competidor']}: {prev_casa} x {prev_visitante} ({pts} pts)\n"

    relatorio += """
━━━━━━━━━━━━━━━━━━
📱 _Relatório automático do Bolão_
"""

    return relatorio


def enviar_whatsapp_contato(numero: str, mensagem: str):
    """
    Envia mensagem para um contato específico

    Args:
        numero: Número com DDD (ex: '+5511999998888')
        mensagem: Texto da mensagem
    """
    import pywhatkit as kit

    try:
        # Envia mensagem instantânea
        kit.sendwhatmsg_instantly(
            phone_no=numero,
            message=mensagem,
            wait_time=15,  # Aguarda 15s para o WhatsApp Web abrir
            tab_close=True  # Fecha a aba depois
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
    print("1. Enviar para WhatsApp do filho")
    print("2. Apenas salvar arquivo")
    print("3. Copiar para área de transferência")

    opcao = input("\nEscolha (1/2/3): ").strip()

    if opcao == "1":
        # Número do filho (com DDD e código do país)
        numero_padrao = "+5511999998888"  # ← TROQUE AQUI

        numero = input(f"Número do WhatsApp (ex: {numero_padrao}): ").strip()
        if not numero:
            numero = numero_padrao

        print(f"\n📱 Enviando para {numero}...")
        print("⚠️  O WhatsApp Web vai abrir. Não mexa no mouse!")
        print("⚠️  Mantenha o WhatsApp Web logado no navegador.")

        enviar_whatsapp_contato(numero, relatorio)

    elif opcao == "2":
        salvar_relatorio(relatorio)

    elif opcao == "3":
        # Copia para área de transferência
        try:
            import pyperclip

            pyperclip.copy(relatorio)
            print("✅ Relatório copiado! Cole no WhatsApp Web.")
        except:
            print("❌ pyperclip não instalado. Instale com: pip install pyperclip")
            salvar_relatorio(relatorio)
    else:
        print("Opção inválida!")