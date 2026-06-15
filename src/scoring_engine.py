"""Módulo: scoring_engine.py"""
# Em desenvolvimento...
# src/scoring_engine.py
"""
Motor de Pontuação do Bolão Copa 2026
Calcula pontos baseado nos palpites vs resultados reais

Regras:
- Acertou o resultado (vitória/empate/derrota): 15 pontos
- Acertou o placar exato: 30 pontos
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import sys

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))


class ScoreRules:
    """Regras de pontuação do bolão"""

    ACERTOU_RESULTADO = 15  # Acertou quem ganhou ou empate
    ACERTOU_PLACAR = 30  # Acertou placar exato (já inclui o resultado)

    @classmethod
    def get_rules_description(cls) -> str:
        """Retorna descrição das regras"""
        return f"""
        📋 REGRAS DE PONTUAÇÃO:
        • Acertou o resultado (vitória/empate/derrota): {cls.ACERTOU_RESULTADO} pontos
        • Acertou o placar exato: {cls.ACERTOU_PLACAR} pontos

        ⚠️  Placar exato já inclui os pontos do resultado.
        Exemplo: Palpite 2x1 e resultado 2x1 = {cls.ACERTOU_PLACAR} pontos
                 Palpite 1x0 e resultado 2x1 = {cls.ACERTOU_RESULTADO} pontos
                 Palpite 1x1 e resultado 2x1 = 0 pontos
        """


class ScoringEngine:
    """
    Calcula a pontuação dos competidores

    Uso:
        engine = ScoringEngine()

        # Calcular pontuação
        df_pontuado = engine.calculate_scores(predictions_df, results_df)

        # Ver ranking
        leaderboard = engine.get_leaderboard(df_pontuado)

        # Detalhes de um competidor
        detalhes = engine.get_competitor_details(df_pontuado, 'João')
    """

    def __init__(self, rules: ScoreRules = None):
        """
        Inicializa o motor de pontuação

        Args:
            rules: Regras de pontuação (usa padrão se None)
        """
        self.rules = rules or ScoreRules()

        # Estatísticas de processamento
        self.stats = {
            'total_jogos_avaliados': 0,
            'total_palpites_processados': 0,
            'placares_exatos': 0,
            'resultados_corretos': 0,
            'pontos_distribuidos': 0,
            'data_calculo': None
        }

    def _determine_result(self, gols_casa: int, gols_visitante: int) -> str:
        """
        Determina o resultado de um jogo

        Args:
            gols_casa: Gols do time da casa
            gols_visitante: Gols do time visitante

        Returns:
            'casa' (vitória casa), 'empate', ou 'fora' (vitória visitante)
        """
        if gols_casa > gols_visitante:
            return 'casa'
        elif gols_casa < gols_visitante:
            return 'fora'
        else:
            return 'empate'

    def _check_result_match(self, pred_casa: int, pred_visitante: int,
                            real_casa: int, real_visitante: int) -> bool:
        """
        Verifica se acertou o resultado (quem ganhou ou empate)

        Args:
            pred_casa: Placar casa previsto
            pred_visitante: Placar visitante previsto
            real_casa: Placar casa real
            real_visitante: Placar visitante real

        Returns:
            True se acertou o resultado
        """
        resultado_previsto = self._determine_result(pred_casa, pred_visitante)
        resultado_real = self._determine_result(real_casa, real_visitante)

        return resultado_previsto == resultado_real

    def _check_exact_score(self, pred_casa: int, pred_visitante: int,
                           real_casa: int, real_visitante: int) -> bool:
        """
        Verifica se acertou o placar exato

        Args:
            pred_casa: Placar casa previsto
            pred_visitante: Placar visitante previsto
            real_casa: Placar casa real
            real_visitante: Placar visitante real

        Returns:
            True se acertou o placar exato
        """
        return (pred_casa == real_casa) and (pred_visitante == real_visitante)

    def _calculate_match_points(self, pred_casa: int, pred_visitante: int,
                                real_casa: int, real_visitante: int) -> Tuple[int, bool, bool]:
        """
        Calcula pontuação de um jogo específico

        Args:
            pred_casa: Placar casa previsto
            pred_visitante: Placar visitante previsto
            real_casa: Placar casa real
            real_visitante: Placar visitante real

        Returns:
            Tupla (pontos, acertou_placar, acertou_resultado)
        """
        # Verifica placar exato primeiro (vale mais)
        acertou_placar = self._check_exact_score(
            pred_casa, pred_visitante, real_casa, real_visitante
        )

        if acertou_placar:
            return self.rules.ACERTOU_PLACAR, True, True

        # Verifica resultado
        acertou_resultado = self._check_result_match(
            pred_casa, pred_visitante, real_casa, real_visitante
        )

        if acertou_resultado:
            return self.rules.ACERTOU_RESULTADO, False, True

        # Não acertou nada
        return 0, False, False

    def calculate_scores(self, predictions: pd.DataFrame,
                         real_results: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula pontuação cruzando previsões com resultados reais

        Args:
            predictions: DataFrame com palpites dos competidores
            real_results: DataFrame com resultados reais

        Returns:
            DataFrame com pontuação calculada
        """
        if predictions.empty:
            print("❌ DataFrame de previsões vazio!")
            return pd.DataFrame()

        if real_results.empty:
            print("❌ DataFrame de resultados vazio!")
            return pd.DataFrame()

        print("\n🧮 Calculando pontuações...")
        print("=" * 50)

        # Prepara dados
        pred = predictions.copy()
        results = real_results.copy()

        # Padroniza nomes dos times (remove espaços extras, maiúsculas)
        for df in [pred, results]:
            for col in ['time_casa', 'time_visitante']:
                if col in df.columns:
                    df[col] = df[col].str.strip()

        # Prepara results com colunas renomeadas ANTES do merge
        results_renamed = results[['time_casa', 'time_visitante', 'placar_casa', 'placar_visitante']].copy()
        results_renamed.columns = ['time_casa', 'time_visitante', 'placar_casa_real', 'placar_visitante_real']

        # Merge (cruza palpites com resultados)
        scored = pred.merge(
            results_renamed,
            on=['time_casa', 'time_visitante'],
            how='inner'
        )

        if scored.empty:
            print("⚠️  Nenhum jogo encontrado em comum!")
            print("   Verifique se os nomes dos times estão iguais nas duas bases")
            return pd.DataFrame()

        # Converte colunas de placar para inteiro
        for col in ['placar_casa_previsto', 'placar_visitante_previsto',
                     'placar_casa_real', 'placar_visitante_real']:
            if col in scored.columns:
                scored[col] = pd.to_numeric(scored[col], errors='coerce').fillna(0).astype(int)
            else:
                # Tenta encontrar com sufixo
                if col == 'placar_casa_real' and 'placar_casa' in scored.columns:
                    scored['placar_casa_real'] = pd.to_numeric(scored['placar_casa'], errors='coerce').fillna(0).astype(int)
                elif col == 'placar_visitante_real' and 'placar_visitante' in scored.columns:
                    scored['placar_visitante_real'] = pd.to_numeric(scored['placar_visitante'], errors='coerce').fillna(0).astype(int)

        # Calcula pontuação linha por linha
        pontos = []
        acertou_placar_list = []
        acertou_resultado_list = []

        for _, row in scored.iterrows():
            pts, placar, resultado = self._calculate_match_points(
                row['placar_casa_previsto'],
                row['placar_visitante_previsto'],
                row['placar_casa_real'],
                row['placar_visitante_real']
            )
            pontos.append(pts)
            acertou_placar_list.append(placar)
            acertou_resultado_list.append(resultado)

        # Adiciona colunas calculadas
        scored['pontos'] = pontos
        scored['acertou_placar'] = acertou_placar_list
        scored['acertou_resultado'] = acertou_resultado_list

        # Adiciona colunas descritivas
        scored['placar_previsto'] = (scored['placar_casa_previsto'].astype(str) +
                                     ' x ' +
                                     scored['placar_visitante_previsto'].astype(str))
        scored['placar_real'] = (scored['placar_casa_real'].astype(str) +
                                 ' x ' +
                                 scored['placar_visitante_real'].astype(str))

        # Adiciona diferença de gols para análise
        scored['diferenca_gols_prevista'] = (scored['placar_casa_previsto'] -
                                             scored['placar_visitante_previsto'])
        scored['diferenca_gols_real'] = (scored['placar_casa_real'] -
                                         scored['placar_visitante_real'])

        # Atualiza estatísticas
        self.stats['total_jogos_avaliados'] = len(scored['match_id'].unique()) if 'match_id' in scored.columns else len(
            scored)
        self.stats['total_palpites_processados'] = len(scored)
        self.stats['placares_exatos'] = scored['acertou_placar'].sum()
        self.stats['resultados_corretos'] = scored['acertou_resultado'].sum()
        self.stats['pontos_distribuidos'] = scored['pontos'].sum()
        self.stats['data_calculo'] = datetime.now().isoformat()

        # Mostra resumo
        print(f"✅ Jogos avaliados: {self.stats['total_jogos_avaliados']}")
        print(f"✅ Palpites processados: {self.stats['total_palpites_processados']}")
        print(f"✅ Placar exato: {self.stats['placares_exatos']}")
        print(f"✅ Resultados corretos: {self.stats['resultados_corretos']}")
        print(f"✅ Total de pontos: {self.stats['pontos_distribuidos']}")

        return scored

    def get_leaderboard(self, scored_df: pd.DataFrame) -> pd.DataFrame:
        """
        Gera ranking dos competidores

        Args:
            scored_df: DataFrame com pontuação calculada

        Returns:
            DataFrame com ranking ordenado
        """
        if scored_df.empty:
            return pd.DataFrame()

        # Agrupa por competidor
        leaderboard = scored_df.groupby('competidor').agg(
            pontos_total=('pontos', 'sum'),
            jogos_avaliados=('pontos', 'count'),
            placares_exatos=('acertou_placar', 'sum'),
            resultados_corretos=('acertou_resultado', 'sum'),
            media_pontos=('pontos', 'mean'),
            max_pontos_jogo=('pontos', 'max'),
            aproveitamento=('pontos', lambda x: (x > 0).sum() / len(x) * 100)
        ).reset_index()

        # Converte para inteiro
        leaderboard['pontos_total'] = leaderboard['pontos_total'].astype(int)
        leaderboard['placares_exatos'] = leaderboard['placares_exatos'].astype(int)
        leaderboard['resultados_corretos'] = leaderboard['resultados_corretos'].astype(int)

        # Arredonda
        leaderboard['media_pontos'] = leaderboard['media_pontos'].round(1)
        leaderboard['aproveitamento'] = leaderboard['aproveitamento'].round(1)

        # Ordena por pontuação (decrescente)
        leaderboard = leaderboard.sort_values(
            ['pontos_total', 'placares_exatos', 'media_pontos'],
            ascending=[False, False, False]
        )

        # Adiciona posição
        leaderboard['posicao'] = range(1, len(leaderboard) + 1)

        # Adiciona diferença para o líder
        if len(leaderboard) > 0:
            pontos_lider = leaderboard.iloc[0]['pontos_total']
            leaderboard['diferenca_lider'] = leaderboard['pontos_total'].apply(
                lambda x: pontos_lider - x
            )

        # Reordena colunas
        cols_order = [
            'posicao', 'competidor', 'pontos_total', 'diferenca_lider',
            'jogos_avaliados', 'placares_exatos', 'resultados_corretos',
            'media_pontos', 'max_pontos_jogo', 'aproveitamento'
        ]

        return leaderboard[[c for c in cols_order if c in leaderboard.columns]]

    def get_competitor_details(self, scored_df: pd.DataFrame,
                               competidor: str) -> pd.DataFrame:
        """
        Detalha previsões de um competidor específico

        Args:
            scored_df: DataFrame com pontuação
            competidor: Nome do competidor

        Returns:
            DataFrame com detalhes do competidor
        """
        if scored_df.empty:
            return pd.DataFrame()

        # Filtra competidor
        details = scored_df[scored_df['competidor'] == competidor].copy()

        if details.empty:
            print(f"❌ Competidor '{competidor}' não encontrado!")
            return pd.DataFrame()

        # Ordena por data se disponível
        if 'data_jogo' in details.columns:
            details = details.sort_values('data_jogo')
        elif 'data' in details.columns:
            details = details.sort_values('data')

        # Seleciona colunas relevantes
        cols = [
            'grupo', 'rodada', 'time_casa', 'time_visitante',
            'placar_previsto', 'placar_real', 'pontos',
            'acertou_placar', 'acertou_resultado'
        ]

        return details[[c for c in cols if c in details.columns]]

    def get_group_analysis(self, scored_df: pd.DataFrame) -> pd.DataFrame:
        """
        Análise de acertos por grupo

        Args:
            scored_df: DataFrame com pontuação

        Returns:
            DataFrame com análise por grupo
        """
        if scored_df.empty or 'grupo' not in scored_df.columns:
            return pd.DataFrame()

        group_analysis = scored_df.groupby('grupo').agg(
            total_palpites=('pontos', 'count'),
            total_pontos=('pontos', 'sum'),
            placares_exatos=('acertou_placar', 'sum'),
            resultados_corretos=('acertou_resultado', 'sum'),
            media_pontos=('pontos', 'mean')
        ).reset_index()

        group_analysis['media_pontos'] = group_analysis['media_pontos'].round(1)
        group_analysis['taxa_acerto'] = (
                group_analysis['resultados_corretos'] / group_analysis['total_palpites'] * 100
        ).round(1)

        return group_analysis.sort_values('total_pontos', ascending=False)

    def get_match_summary(self, scored_df: pd.DataFrame) -> pd.DataFrame:
        """
        Resumo por jogo: quantos acertaram cada resultado

        Args:
            scored_df: DataFrame com pontuação

        Returns:
            DataFrame com resumo por jogo
        """
        if scored_df.empty:
            return pd.DataFrame()

        match_summary = scored_df.groupby(
            ['time_casa', 'time_visitante', 'placar_real']
        ).agg(
            total_palpites=('competidor', 'count'),
            acertaram_placar=('acertou_placar', 'sum'),
            acertaram_resultado=('acertou_resultado', 'sum'),
            pontos_medios=('pontos', 'mean')
        ).reset_index()

        match_summary['pontos_medios'] = match_summary['pontos_medios'].round(1)

        # Ordena por mais acertos de placar
        match_summary = match_summary.sort_values(
            ['acertaram_placar', 'acertaram_resultado'],
            ascending=[False, False]
        )

        return match_summary

    def save_results(self, scored_df: pd.DataFrame,
                     filepath: str = "data/pontuacao_completa.csv"):
        """
        Salva pontuação calculada

        Args:
            scored_df: DataFrame com pontuação
            filepath: Caminho para salvar
        """
        if scored_df.empty:
            print("❌ Nada para salvar!")
            return

        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        scored_df.to_csv(filepath, index=False, encoding='utf-8')
        print(f"💾 Pontuação salva em: {filepath}")

    def print_leaderboard(self, leaderboard: pd.DataFrame):
        """
        Imprime o ranking de forma formatada

        Args:
            leaderboard: DataFrame do ranking
        """
        if leaderboard.empty:
            print("❌ Ranking vazio!")
            return

        print("\n" + "=" * 70)
        print("🏆 RANKING DO BOLÃO - COPA 2026")
        print("=" * 70)

        medals = {1: '🥇', 2: '🥈', 3: '🥉'}

        for _, row in leaderboard.iterrows():
            pos = int(row['posicao'])
            medal = medals.get(pos, f'{pos}º')

            print(f"\n{medal} {row['competidor']}")
            print(f"   Pontos: {row['pontos_total']}")
            print(f"   Placar exato: {row['placares_exatos']}")
            print(f"   Resultados corretos: {row['resultados_corretos']}")
            print(f"   Média: {row['media_pontos']} pts/jogo")
            print(f"   Aproveitamento: {row['aproveitamento']}%")

            if 'diferenca_lider' in row and row['diferenca_lider'] > 0:
                print(f"   ⬇ {row['diferenca_lider']} pontos atrás do líder")

        print("\n" + "=" * 70)

    def get_stats(self) -> Dict:
        """Retorna estatísticas do último cálculo"""
        return self.stats


# ============================================
# FUNÇÕES DE TESTE
# ============================================

def test_scoring_engine():
    """Testa o motor de pontuação com dados de exemplo"""

    print("\n" + "🏆" * 20)
    print("   MOTOR DE PONTUAÇÃO - COPA 2026")
    print("🏆" * 20)

    # Mostra regras
    print(ScoreRules.get_rules_description())

    # Cria dados de exemplo
    print("\n📊 Criando dados de teste...")

    # Previsões mock
    predictions_data = {
        'competidor': ['João', 'João', 'João', 'Maria', 'Maria', 'Maria'],
        'grupo': ['A', 'A', 'B', 'A', 'A', 'B'],
        'time_casa': ['México', 'Coreia do Sul', 'Brasil',
                      'México', 'Coreia do Sul', 'Brasil'],
        'time_visitante': ['África do Sul', 'República Tcheca', 'Marrocos',
                           'África do Sul', 'República Tcheca', 'Marrocos'],
        'placar_casa_previsto': [2, 1, 2, 2, 2, 1],
        'placar_visitante_previsto': [0, 1, 0, 0, 1, 1]
    }
    predictions_df = pd.DataFrame(predictions_data)

    # Resultados reais mock
    results_data = {
        'time_casa': ['México', 'Coreia do Sul', 'Brasil'],
        'time_visitante': ['África do Sul', 'República Tcheca', 'Marrocos'],
        'placar_casa': [2, 2, 1],
        'placar_visitante': [0, 1, 1]
    }
    results_df = pd.DataFrame(results_data)

    print(f"✅ Previsões: {len(predictions_df)} palpites")
    print(f"✅ Resultados: {len(results_df)} jogos")

    # Cria engine e calcula
    engine = ScoringEngine()
    scored = engine.calculate_scores(predictions_df, results_df)

    if not scored.empty:
        print("\n📋 Amostra dos resultados:")
        print(scored[['competidor', 'time_casa', 'time_visitante',
                      'placar_previsto', 'placar_real', 'pontos']].to_string())

        # Ranking
        leaderboard = engine.get_leaderboard(scored)
        engine.print_leaderboard(leaderboard)

        # Detalhes do João
        print("\n🔍 Detalhes do João:")
        joao_details = engine.get_competitor_details(scored, 'João')
        print(joao_details.to_string())

    return engine, scored


# ============================================
# EXECUÇÃO DIRETA
# ============================================
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🧪 TESTE DO MOTOR DE PONTUAÇÃO")
    print("=" * 60)

    engine, scored = test_scoring_engine()

    if scored is not None and not scored.empty:
        print("\n✅ Teste concluído com sucesso!")
        print("\n💡 Para usar com dados reais:")
        print("   from scoring_engine import ScoringEngine")
        print("   engine = ScoringEngine()")
        print("   resultado = engine.calculate_scores(predictions_df, results_df)")
        print("   ranking = engine.get_leaderboard(resultado)")
    else:
        print("\n❌ Falha no teste!")