"""Módulo: process_predictions.py"""
# Em desenvolvimento...
# src/process_predictions.py
"""
Processador de Planilhas dos Competidores
Lê, valida e consolida as planilhas de palpites
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import re
import sys

# Adiciona o diretório raiz ao path para imports
sys.path.append(str(Path(__file__).parent.parent))


class PredictionProcessor:
    """
    Processa as planilhas Excel dos competidores e consolida em um único DataFrame

    Uso:
        processor = PredictionProcessor()
        df = processor.consolidate_predictions()
        print(f"Total de palpites: {len(df)}")
    """

    def __init__(self, predictions_folder: str = "planilhas_competidores"):
        """
        Inicializa o processador

        Args:
            predictions_folder: Caminho da pasta com as planilhas
        """
        # Garante caminho relativo à raiz do projeto
        self.project_root = Path(__file__).parent.parent
        self.predictions_folder = self.project_root / predictions_folder

        self.prediction_columns = [
            'competidor',
            'grupo',
            'rodada',
            'data_jogo',
            'hora_jogo',
            'time_casa',
            'time_visitante',
            'cidade',
            'placar_casa_previsto',
            'placar_visitante_previsto'
        ]

        # Mapeamento de possíveis nomes de colunas
        self.column_mapping = {
            'grupo': ['grupo', 'group', 'grp'],
            'rodada': ['rodada', 'round', 'rd', 'rod'],
            'data': ['data', 'date', 'dt', 'dia'],
            'hora': ['hora', 'hour', 'hr', 'horário', 'horario'],
            'time_casa': ['time_casa', 'time casa', 'home', 'mandante', 'casa'],
            'time_visitante': ['time_visitante', 'time visitante', 'away', 'visitante', 'fora'],
            'cidade': ['cidade', 'city', 'local', 'sede'],
            'placar_casa_previsto': ['placar_casa_previsto', 'placar casa previsto',
                                     'placar_casa', 'placar casa', 'gols_casa',
                                     'gols casa', 'previsto_casa'],
            'placar_visitante_previsto': ['placar_visitante_previsto', 'placar visitante previsto',
                                          'placar_visitante', 'placar visitante', 'gols_visitante',
                                          'gols visitante', 'previsto_visitante'],
        }

        # Estatísticas
        self.stats = {
            'total_planilhas': 0,
            'planilhas_processadas': 0,
            'planilhas_com_erro': 0,
            'total_palpites': 0,
            'erros': []
        }

    def _normalize_column_name(self, col_name: str) -> str:
        """
        Normaliza o nome da coluna para o padrão do sistema

        Args:
            col_name: Nome original da coluna

        Returns:
            Nome padronizado
        """
        # Converte para minúsculas e remove acentos
        col = col_name.lower().strip()
        col = col.replace('ç', 'c').replace('ã', 'a').replace('á', 'a')
        col = col.replace('é', 'e').replace('í', 'i').replace('ó', 'o')
        col = col.replace('ú', 'u').replace('õ', 'o').replace('ê', 'e')

        # Remove caracteres especiais
        col = re.sub(r'[^a-z0-9\s]', '', col)
        # Substitui múltiplos espaços por um
        col = re.sub(r'\s+', '_', col)

        return col

    def _match_column(self, col_name: str) -> Optional[str]:
        """
        Tenta encontrar o nome padronizado da coluna

        Args:
            col_name: Nome da coluna na planilha

        Returns:
            Nome padronizado ou None se não encontrar
        """
        col_normalized = self._normalize_column_name(col_name)

        # Procura nos mapeamentos
        for standard_name, possible_names in self.column_mapping.items():
            for possible in possible_names:
                possible_norm = self._normalize_column_name(possible)
                if col_normalized == possible_norm:
                    return standard_name

        return None

    def _extract_competitor_name(self, file_path: Path) -> str:
        """
        Extrai o nome do competidor do nome do arquivo

        Args:
            file_path: Caminho do arquivo

        Returns:
            Nome do competidor
        """
        # Remove extensão
        name = file_path.stem

        # Tenta extrair nome antes de "previsoes" ou "_"
        patterns = [
            r'^(.+?)_previsoes',
            r'^(.+?)_palpites',
            r'^(.+?)_copa',
            r'^(.+?)_2026',
        ]

        for pattern in patterns:
            match = re.search(pattern, name, re.IGNORECASE)
            if match:
                return match.group(1).replace('_', ' ').title()

        # Se não encontrou padrão, usa o nome do arquivo
        name = name.replace('_', ' ').replace('-', ' ')
        return name.title()

    def load_competitor_sheet(self, file_path: Path) -> Optional[pd.DataFrame]:
        """
        Carrega e processa a planilha de um competidor

        Args:
            file_path: Caminho do arquivo Excel

        Returns:
            DataFrame processado ou None se erro
        """
        try:
            # Lê o arquivo Excel
            df = pd.read_excel(file_path, dtype=str)

            # Extrai nome do competidor
            competidor = self._extract_competitor_name(file_path)

            # Padroniza nomes das colunas
            new_columns = {}
            colunas_nao_mapeadas = []

            for col in df.columns:
                mapped = self._match_column(col)
                if mapped:
                    new_columns[col] = mapped
                else:
                    colunas_nao_mapeadas.append(col)

            # Verifica se encontrou colunas essenciais
            essential = ['time_casa', 'time_visitante',
                         'placar_casa_previsto', 'placar_visitante_previsto']
            mapped_essential = [new_columns.get(c, c) for c in df.columns]

            missing = [e for e in essential if e not in mapped_essential
                       and e not in new_columns.values()]

            if missing:
                print(f"⚠️  Colunas essenciais não encontradas em {file_path.name}: {missing}")
                print(f"   Colunas encontradas: {list(df.columns)}")
                return None

            # Renomeia colunas
            df = df.rename(columns=new_columns)

            # Adiciona colunas do competidor e metadados
            df['competidor'] = competidor
            df['arquivo_origem'] = file_path.name

            # Garante que colunas de placar são numéricas
            for col in ['placar_casa_previsto', 'placar_visitante_previsto']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            # Converte data se existir
            if 'data' in df.columns:
                df['data_jogo'] = pd.to_datetime(df['data'], format='mixed', dayfirst=True)
                df = df.drop(columns=['data'])

            # Adiciona colunas faltantes com valor padrão
            for col in self.prediction_columns:
                if col not in df.columns:
                    df[col] = None

            # Seleciona e ordena colunas
            cols_to_keep = [c for c in self.prediction_columns if c in df.columns]

            # Garante que a coluna arquivo_origem seja mantida
            if 'arquivo_origem' in df.columns:
                cols_to_keep.append('arquivo_origem')

            return df[cols_to_keep]

        except Exception as e:
            print(f"❌ Erro ao processar {file_path.name}: {e}")
            return None

    def _validate_competitor_data(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Valida os dados de um competidor

        Args:
            df: DataFrame do competidor

        Returns:
            Tupla (é_válido, lista_de_erros)
        """
        errors = []

        # Verifica número de jogos
        expected_games = 72  # 12 grupos x 6 jogos
        if len(df) != expected_games:
            errors.append(
                f"Número incorreto de jogos: {len(df)} (esperado: {expected_games})"
            )

        # Verifica se há palpites preenchidos
        palpites_preenchidos = (
                df['placar_casa_previsto'].notna().sum() +
                df['placar_visitante_previsto'].notna().sum()
        )

        if palpites_preenchidos == 0:
            errors.append("Nenhum palpite preenchido")

        # Verifica valores negativos
        for col in ['placar_casa_previsto', 'placar_visitante_previsto']:
            if col in df.columns:
                negativos = (df[col] < 0).sum()
                if negativos > 0:
                    errors.append(f"{negativos} valores negativos em {col}")

        # Verifica valores muito altos (>20 gols)
        for col in ['placar_casa_previsto', 'placar_visitante_previsto']:
            if col in df.columns:
                altos = (df[col] > 20).sum()
                if altos > 0:
                    errors.append(f"{altos} valores maiores que 20 em {col}")

        return len(errors) == 0, errors

    def consolidate_predictions(self) -> pd.DataFrame:
        """
        Consolida todas as planilhas em um único DataFrame

        Returns:
            DataFrame com todos os palpites consolidados
        """
        all_predictions = []

        # Verifica se a pasta existe
        if not self.predictions_folder.exists():
            print(f"❌ Pasta '{self.predictions_folder}' não encontrada!")
            return pd.DataFrame()

        # Lista todos os arquivos Excel
        excel_files = list(self.predictions_folder.glob('*.xlsx')) + \
                      list(self.predictions_folder.glob('*.xls'))

        # Remove templates
        excel_files = [f for f in excel_files
                       if 'template' not in f.name.lower()]

        self.stats['total_planilhas'] = len(excel_files)

        print(f"\n📋 Processando {len(excel_files)} planilhas...")
        print("=" * 60)

        for file_path in sorted(excel_files):
            print(f"\n📄 {file_path.name}")
            print(f"   Competidor: {self._extract_competitor_name(file_path)}")

            # Carrega planilha
            df = self.load_competitor_sheet(file_path)

            if df is not None:
                # Valida dados
                is_valid, errors = self._validate_competitor_data(df)

                if errors:
                    print(f"   ⚠️  Avisos:")
                    for error in errors:
                        print(f"      - {error}")

                all_predictions.append(df)
                self.stats['planilhas_processadas'] += 1
                palpites = df['placar_casa_previsto'].notna().sum()
                print(f"   ✅ Processado: {palpites} palpites preenchidos")
            else:
                self.stats['planilhas_com_erro'] += 1
                error_msg = f"Erro ao processar {file_path.name}"
                self.stats['erros'].append(error_msg)
                print(f"   ❌ {error_msg}")

        # Consolida
        if all_predictions:
            consolidated = pd.concat(all_predictions, ignore_index=True)
            self.stats['total_palpites'] = len(consolidated)

            print("\n" + "=" * 60)
            print("✅ CONSOLIDAÇÃO CONCLUÍDA")
            print(f"   Planilhas processadas: {self.stats['planilhas_processadas']}/{self.stats['total_planilhas']}")
            print(f"   Total de palpites: {self.stats['total_palpites']}")
            print(f"   Competidores: {consolidated['competidor'].nunique()}")

            if self.stats['erros']:
                print(f"\n   ⚠️  Erros encontrados: {len(self.stats['erros'])}")
                for erro in self.stats['erros']:
                    print(f"      - {erro}")

            return consolidated
        else:
            print("\n❌ Nenhuma planilha válida encontrada!")
            return pd.DataFrame()

    def get_competitors_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Gera resumo dos palpites por competidor

        Args:
            df: DataFrame consolidado

        Returns:
            DataFrame com resumo
        """
        if df.empty:
            return pd.DataFrame()

        summary = df.groupby('competidor').agg(
            palpites_preenchidos=('placar_casa_previsto', 'count'),
            media_gols_casa=('placar_casa_previsto', 'mean'),
            media_gols_visitante=('placar_visitante_previsto', 'mean'),
            arquivo_origem=('arquivo_origem', 'first')
        ).reset_index()

        summary['media_gols_casa'] = summary['media_gols_casa'].round(1)
        summary['media_gols_visitante'] = summary['media_gols_visitante'].round(1)

        return summary

    def save_consolidated(self, df: pd.DataFrame, filepath: str = "data/previsoes_consolidadas.csv"):
        """
        Salva os dados consolidados em CSV

        Args:
            df: DataFrame consolidado
            filepath: Caminho para salvar
        """
        if df.empty:
            print("❌ DataFrame vazio, nada para salvar")
            return

        # Garante que o diretório existe
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        # Salva
        df.to_csv(filepath, index=False, encoding='utf-8')
        print(f"\n💾 Dados salvos em: {filepath}")
        print(f"   Registros: {len(df)}")
        print(f"   Colunas: {list(df.columns)}")

    def print_summary(self):
        """Imprime resumo das estatísticas"""
        print("\n" + "=" * 60)
        print("📊 RESUMO DO PROCESSAMENTO")
        print("=" * 60)
        print(f"Total de planilhas encontradas: {self.stats['total_planilhas']}")
        print(f"Planilhas processadas com sucesso: {self.stats['planilhas_processadas']}")
        print(f"Planilhas com erro: {self.stats['planilhas_com_erro']}")
        print(f"Total de palpites consolidados: {self.stats['total_palpites']}")

        if self.stats['erros']:
            print(f"\nErros detalhados:")
            for erro in self.stats['erros']:
                print(f"  - {erro}")


def test_processor():
    """Função para testar o processador"""

    print("\n" + "=" * 60)
    print("🧪 TESTE DO PROCESSADOR DE PLANILHAS")
    print("=" * 60)

    # Cria processador
    processor = PredictionProcessor()

    # Processa planilhas
    df = processor.consolidate_predictions()

    if not df.empty:
        # Mostra amostra
        print("\n📋 Amostra dos dados:")
        print(df.head(10).to_string())

        # Resumo por competidor
        print("\n👥 Resumo por Competidor:")
        summary = processor.get_competitors_summary(df)
        print(summary.to_string())

        # Salva dados
        processor.save_consolidated(df)

        # Estatísticas
        processor.print_summary()

        return df
    else:
        print("\n⚠️  Nenhum dado para mostrar!")
        print("Verifique se existem planilhas na pasta 'planilhas_competidores/'")
        return None


# ============================================
# EXECUÇÃO DIRETA
# ============================================
if __name__ == "__main__":
    print("\n" + "🏆" * 20)
    print("   PROCESSADOR DE PLANILHAS - COPA 2026")
    print("🏆" * 20)

    # Testa o processador
    df_resultado = test_processor()

    if df_resultado is not None:
        print("\n✅ Processamento concluído com sucesso!")
    else:
        print("\n❌ Falha no processamento!")