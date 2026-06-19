"""Módulo: manual_results.py"""
# Em desenvolvimento...
# src/manual_results.py
"""
Sistema de Atualização Manual de Resultados
Permite cadastrar e gerenciar os resultados reais dos jogos
Sem dependência de APIs externas
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, List, Optional, Tuple
import sys

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

# Importa os dados oficiais da Copa
try:
    from copa2026_data import JOGOS_FASE_GRUPOS
except ImportError:
    print("⚠️  Módulo copa2026_data.py não encontrado!")
    print("   Execute primeiro: python utils/create_template.py")
    JOGOS_FASE_GRUPOS = []


class ManualResultsManager:
    """
    Gerenciador de resultados manuais dos jogos

    Uso:
        manager = ManualResultsManager()

        # Cadastrar resultado
        manager.update_result('A_1_México_vs_África do Sul', 2, 0)

        # Ver todos os resultados
        df = manager.get_all_results_as_dataframe()

        # Ver progresso
        progresso = manager.get_progress()
    """

    def __init__(self, results_file: str = "data/resultados_oficiais.json"):
        """
        Inicializa o gerenciador

        Args:
            results_file: Caminho do arquivo JSON com resultados
        """
        self.results_file = Path(results_file)

        # Garante que o diretório existe
        self.results_file.parent.mkdir(parents=True, exist_ok=True)

        # Carrega dados dos jogos PRIMEIRO
        self.jogos = JOGOS_FASE_GRUPOS

        # Inicializa results VAZIO
        self.results = {}

        # Estatísticas
        self.stats = {
            'total_jogos': len(self.jogos),
            'jogos_realizados': 0,
            'jogos_pendentes': 0,
            'total_gols': 0,
            'media_gols': 0.0
        }

        # Carrega resultados existentes (agora self.jogos já existe)
        self.load_results()

        # Atualiza estatísticas
        self._update_stats()

    def _generate_match_id(self, jogo: Dict) -> str:
        """
        Gera ID único para cada jogo

        Args:
            jogo: Dicionário com dados do jogo

        Returns:
            ID único do jogo
        """
        grupo = jogo.get('grupo', '')
        rodada = jogo.get('rodada', '')
        casa = jogo.get('casa', '')
        visitante = jogo.get('visitante', '')

        # Formato: A_R1_México_vs_África do Sul
        return f"{grupo}_R{rodada}_{casa}_vs_{visitante}"

    def load_results(self) -> Dict:
        """
        Carrega resultados salvos do arquivo JSON

        Returns:
            Dicionário com resultados
        """
        if self.results_file.exists():
            try:
                with open(self.results_file, 'r', encoding='utf-8') as f:
                    self.results = json.load(f)
                print(f"📂 Resultados carregados: {len(self.results)} jogos")
            except Exception as e:
                print(f"⚠️  Erro ao carregar resultados: {e}")
                self.results = {}
        else:
            print("📝 Nenhum resultado anterior encontrado. Iniciando novo arquivo.")
            self.results = {}
            self._initialize_results()

        return self.results

    def _initialize_results(self):
        """Inicializa estrutura de resultados vazia"""
        for jogo in self.jogos:
            match_id = self._generate_match_id(jogo)

            # Verifica se o jogo já tem placar nos dados originais
            if jogo.get('placar_casa') is not None and jogo.get('placar_visitante') is not None:
                self.results[match_id] = {
                    'placar_casa': jogo['placar_casa'],
                    'placar_visitante': jogo['placar_visitante'],
                    'atualizado_em': datetime.now().isoformat(),
                    'status': 'Realizado',
                    'grupo': jogo['grupo'],
                    'rodada': jogo['rodada'],
                    'data': jogo['data'],
                    'hora': jogo.get('hora', ''),
                    'casa': jogo['casa'],
                    'visitante': jogo['visitante'],
                    'cidade': jogo.get('cidade', '')
                }
            else:
                self.results[match_id] = {
                    'placar_casa': None,
                    'placar_visitante': None,
                    'atualizado_em': None,
                    'status': 'Pendente',
                    'grupo': jogo['grupo'],
                    'rodada': jogo['rodada'],
                    'data': jogo['data'],
                    'hora': jogo.get('hora', ''),
                    'casa': jogo['casa'],
                    'visitante': jogo['visitante'],
                    'cidade': jogo.get('cidade', '')
                }

        self.save_results()

    def save_results(self):
        """Salva resultados no arquivo JSON"""
        try:
            with open(self.results_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Erro ao salvar resultados: {e}")

    def update_result(self, match_id: str, placar_casa: int,
                      placar_visitante: int) -> bool:
        """
        Atualiza ou cadastra resultado de um jogo

        Args:
            match_id: ID do jogo (ex: 'A_R1_México_vs_África do Sul')
            placar_casa: Gols do time da casa
            placar_visitante: Gols do time visitante

        Returns:
            True se sucesso, False se erro
        """
        if match_id not in self.results:
            print(f"❌ Jogo não encontrado: {match_id}")
            return False

        # Valida os valores
        if not isinstance(placar_casa, int) or not isinstance(placar_visitante, int):
            print("❌ Placar deve ser número inteiro")
            return False

        if placar_casa < 0 or placar_visitante < 0:
            print("❌ Placar não pode ser negativo")
            return False

        if placar_casa > 20 or placar_visitante > 20:
            print("⚠️  Placar muito alto! Confirme se está correto.")

        # Atualiza resultado
        jogo_info = self.results[match_id]
        self.results[match_id] = {
            **jogo_info,
            'placar_casa': placar_casa,
            'placar_visitante': placar_visitante,
            'atualizado_em': datetime.now().isoformat(),
            'status': 'Realizado'
        }

        # Salva
        self.save_results()
        self._update_stats()

        casa = jogo_info.get('casa', '')
        visitante = jogo_info.get('visitante', '')
        print(f"✅ {casa} {placar_casa} x {placar_visitante} {visitante}")

        return True

    def delete_result(self, match_id: str) -> bool:
        """
        Remove um resultado (volta para Pendente)

        Args:
            match_id: ID do jogo

        Returns:
            True se sucesso
        """
        if match_id not in self.results:
            print(f"❌ Jogo não encontrado: {match_id}")
            return False

        self.results[match_id].update({
            'placar_casa': None,
            'placar_visitante': None,
            'atualizado_em': None,
            'status': 'Pendente'
        })

        self.save_results()
        self._update_stats()

        print(f"🔄 Resultado removido: {match_id}")
        return True

    def get_result(self, match_id: str) -> Optional[Dict]:
        """
        Obtém resultado de um jogo específico

        Args:
            match_id: ID do jogo

        Returns:
            Dicionário com resultado ou None
        """
        return self.results.get(match_id)

    def get_results_by_group(self, grupo: str) -> List[Dict]:
        """
        Filtra resultados por grupo

        Args:
            grupo: Letra do grupo (A-L)

        Returns:
            Lista de resultados do grupo
        """
        return [
            {**result, 'match_id': match_id}
            for match_id, result in self.results.items()
            if result.get('grupo') == grupo.upper()
        ]

    def get_results_by_status(self, status: str) -> List[Dict]:
        """
        Filtra resultados por status

        Args:
            status: 'Realizado' ou 'Pendente'

        Returns:
            Lista de resultados com o status
        """
        return [
            {**result, 'match_id': match_id}
            for match_id, result in self.results.items()
            if result.get('status') == status
        ]

    def get_all_results_as_dataframe(self) -> pd.DataFrame:
        """
        Converte todos os resultados para DataFrame

        Returns:
            DataFrame com todos os resultados
        """
        rows = []

        for match_id, result in self.results.items():
            rows.append({
                'match_id': match_id,
                'grupo': result.get('grupo', ''),
                'rodada': result.get('rodada', ''),
                'data': result.get('data', ''),
                'hora': result.get('hora', ''),
                'time_casa': result.get('casa', ''),
                'time_visitante': result.get('visitante', ''),
                'cidade': result.get('cidade', ''),
                'placar_casa': result.get('placar_casa'),
                'placar_visitante': result.get('placar_visitante'),
                'status': result.get('status', 'Pendente'),
                'atualizado_em': result.get('atualizado_em')
            })

        df = pd.DataFrame(rows)

        # Converte data
        if 'data' in df.columns:
            df['data'] = pd.to_datetime(df['data'], errors='coerce')

        return df

    def get_only_completed_results(self) -> pd.DataFrame:
        """Retorna apenas jogos já realizados"""
        df = self.get_all_results_as_dataframe()

        # Mostra colunas disponíveis (para debug)
        print(f"Colunas disponíveis: {list(df.columns)}")

        # Tenta encontrar a coluna correta
        if 'status' in df.columns:
            return df[df['status'] == 'Realizado'].copy()
        elif 'placar_casa' in df.columns:
            return df[df['placar_casa'].notna()].copy()
        elif 'placar_casa_real' in df.columns:
            return df[df['placar_casa_real'].notna()].copy()
        else:
            # Retorna tudo se não encontrar coluna de filtro
            return df

    def get_progress(self) -> Dict:
        """
        Retorna progresso do cadastro de resultados

        Returns:
            Dicionário com estatísticas de progresso
        """
        total = self.stats['total_jogos']
        realizados = self.stats['jogos_realizados']
        pendentes = self.stats['jogos_pendentes']

        porcentagem = (realizados / total * 100) if total > 0 else 0

        # Progresso por grupo
        grupos = {}
        for grupo_letra in 'ABCDEFGHIJKL':
            grupo_jogos = self.get_results_by_group(grupo_letra)
            total_grupo = len(grupo_jogos)
            realizados_grupo = sum(1 for j in grupo_jogos if j.get('status') == 'Realizado')

            grupos[grupo_letra] = {
                'total': total_grupo,
                'realizados': realizados_grupo,
                'pendentes': total_grupo - realizados_grupo,
                'porcentagem': (realizados_grupo / total_grupo * 100) if total_grupo > 0 else 0
            }

        return {
            'total_jogos': total,
            'jogos_realizados': realizados,
            'jogos_pendentes': pendentes,
            'porcentagem': round(porcentagem, 1),
            'total_gols': self.stats['total_gols'],
            'media_gols': round(self.stats['media_gols'], 2),
            'por_grupo': grupos
        }

    def _update_stats(self):
        """Atualiza estatísticas internas"""
        realizados = 0
        total_gols = 0

        for result in self.results.values():
            if result.get('status') == 'Realizado':
                realizados += 1
                gols_casa = result.get('placar_casa', 0) or 0
                gols_visitante = result.get('placar_visitante', 0) or 0
                total_gols += gols_casa + gols_visitante

        self.stats['jogos_realizados'] = realizados
        self.stats['jogos_pendentes'] = self.stats['total_jogos'] - realizados
        self.stats['total_gols'] = total_gols
        self.stats['media_gols'] = total_gols / realizados if realizados > 0 else 0

    def print_progress(self):
        """Imprime relatório de progresso"""
        progress = self.get_progress()

        print("\n" + "=" * 60)
        print("📊 PROGRESSO DOS RESULTADOS")
        print("=" * 60)
        print(f"Total de jogos: {progress['total_jogos']}")
        print(f"Jogos realizados: {progress['jogos_realizados']}")
        print(f"Jogos pendentes: {progress['jogos_pendentes']}")
        print(f"Progresso: {progress['porcentagem']}%")
        print(f"Total de gols: {progress['total_gols']}")
        print(f"Média de gols/jogo: {progress['media_gols']}")

        print("\n📋 Por Grupo:")
        for grupo, dados in progress['por_grupo'].items():
            barra = '█' * int(dados['porcentagem'] / 10)
            vazio = '░' * (10 - int(dados['porcentagem'] / 10))
            print(
                f"  Grupo {grupo}: {barra}{vazio} {dados['realizados']}/{dados['total']} ({dados['porcentagem']:.0f}%)")

    def print_pending_matches(self):
        """Lista os próximos jogos pendentes"""
        pendentes = self.get_results_by_status('Pendente')

        if not pendentes:
            print("\n✅ Todos os jogos já foram realizados!")
            return

        print("\n📅 PRÓXIMOS JOGOS PENDENTES:")
        print("-" * 60)

        # Ordena por data
        pendentes_ordenados = sorted(pendentes, key=lambda x: x.get('data', ''))

        for jogo in pendentes_ordenados[:10]:  # Mostra os 10 primeiros
            print(f"  {jogo.get('data', '')} {jogo.get('hora', '')} - "
                  f"Grupo {jogo.get('grupo', '')} - "
                  f"{jogo.get('casa', '')} vs {jogo.get('visitante', '')} - "
                  f"{jogo.get('cidade', '')}")

        if len(pendentes) > 10:
            print(f"  ... e mais {len(pendentes) - 10} jogos")


# ============================================
# FUNÇÕES DE TESTE E DEMONSTRAÇÃO
# ============================================

def test_manager():
    """Testa o gerenciador de resultados"""

    print("\n" + "🏆" * 20)
    print("   GERENCIADOR DE RESULTADOS - COPA 2026")
    print("🏆" * 20)

    # Cria gerenciador
    manager = ManualResultsManager()

    # Mostra progresso
    manager.print_progress()

    # Mostra pendentes
    manager.print_pending_matches()

    # Mostra resultados já cadastrados
    df = manager.get_all_results_as_dataframe()
    realizados = df[df['status'] == 'Realizado']

    if not realizados.empty:
        print("\n📋 JOGOS JÁ REALIZADOS:")
        print("-" * 60)
        for _, jogo in realizados.iterrows():
            print(f"  Grupo {jogo['grupo']} - {jogo['time_casa']} "
                  f"{int(jogo['placar_casa'])} x {int(jogo['placar_visitante'])} "
                  f"{jogo['time_visitante']} ({jogo['data'].strftime('%d/%m/%Y')})")

    return manager


def interactive_update():
    """Modo interativo para cadastrar resultados"""

    print("\n" + "=" * 60)
    print("📝 ATUALIZAÇÃO INTERATIVA DE RESULTADOS")
    print("=" * 60)
    print("Instruções:")
    print("  - Digite o ID do jogo ou parte dele")
    print("  - Digite o placar (ex: 2 1 para 2x1)")
    print("  - Digite 'sair' para terminar")
    print("  - Digite 'lista' para ver pendentes")
    print("=" * 60)

    manager = ManualResultsManager()

    while True:
        print("\n" + "-" * 40)
        comando = input("🔍 Buscar jogo (ou 'sair'/'lista'): ").strip()

        if comando.lower() == 'sair':
            break

        if comando.lower() == 'lista':
            manager.print_pending_matches()
            continue

        # Busca jogos que contenham o texto
        encontrados = []
        for match_id in manager.results:
            if comando.lower() in match_id.lower():
                encontrados.append(match_id)

        if not encontrados:
            print("❌ Nenhum jogo encontrado!")
            continue

        # Mostra encontrados
        print(f"\n📋 {len(encontrados)} jogo(s) encontrado(s):")
        for i, match_id in enumerate(encontrados, 1):
            jogo = manager.results[match_id]
            status = jogo.get('status', 'Pendente')
            placar = f"{jogo.get('placar_casa', '-')} x {jogo.get('placar_visitante', '-')}"
            print(f"  {i}. [{status}] {jogo.get('casa')} {placar} {jogo.get('visitante')} "
                  f"({jogo.get('data')}) - ID: {match_id}")

        # Seleciona jogo
        if len(encontrados) > 1:
            escolha = input(f"\nEscolha o número (1-{len(encontrados)}): ").strip()
            try:
                idx = int(escolha) - 1
                match_id = encontrados[idx]
            except:
                print("❌ Opção inválida!")
                continue
        else:
            match_id = encontrados[0]

        # Pede placar
        placar = input("Placar (casa visitante): ").strip()
        try:
            partes = placar.split()
            if len(partes) == 2:
                casa = int(partes[0])
                visitante = int(partes[1])
                manager.update_result(match_id, casa, visitante)
            else:
                print("❌ Formato inválido! Use: 2 1 (para 2x1)")
        except ValueError:
            print("❌ Use apenas números!")


# ============================================
# EXECUÇÃO DIRETA
# ============================================
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'interativo':
        # Modo interativo
        interactive_update()
    else:
        # Modo teste
        manager = test_manager()

        print("\n" + "=" * 60)
        print("💡 Dicas:")
        print("  - Para atualizar todos os resultados, edite o JSON:")
        print(f"    {manager.results_file}")
        print("  - Para modo interativo: python src/manual_results.py interativo")
        print("=" * 60)