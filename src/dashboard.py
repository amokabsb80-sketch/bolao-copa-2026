"""Módulo: dashboard.py"""
# Em desenvolvimento...
# src/dashboard.py
"""
🏆 DASHBOARD - BOLÃO COPA DO MUNDO | 2026
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
import sys

# Adiciona src ao path
sys.path.append(str(Path(__file__).parent))

# Importa módulos do sistema
from process_predictions import PredictionProcessor
from manual_results import ManualResultsManager
from scoring_engine import ScoringEngine, ScoreRules
from assets_manager import AssetsManager

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="🏆 Bolão Copa 2026",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': 'Bolão Copa do Mundo 2026'
    }
)

# ============================================
# TEMA QUE RESPEITA LIGHT/DARK DO STREAMLIT
# ============================================
st.markdown("""
<style>
    /* ============================================
       TEMA DARK (padrão)
       ============================================ */
    [data-theme="dark"] {
        --bg-primary: #0d1117;
        --bg-secondary: #161b22;
        --bg-card: #161b22;
        --text-primary: #e6edf3;
        --text-secondary: #8b949e;
        --border-color: #30363d;
        --accent: #58a6ff;
        --success: #3fb950;
        --warning: #d29922;
        --danger: #da3633;
    }

    /* ============================================
       TEMA LIGHT
       ============================================ */
    [data-theme="light"] {
        --bg-primary: #ffffff;
        --bg-secondary: #f6f8fa;
        --bg-card: #ffffff;
        --text-primary: #1f2328;
        --text-secondary: #656d76;
        --border-color: #d0d7de;
        --accent: #0969da;
        --success: #1a7f37;
        --warning: #9a6700;
        --danger: #cf222e;
    }

    /* Aplica cores do tema */
    .stApp {
        background: var(--bg-primary);
    }

    /* Textos */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
    }

    p, span, li, label {
        color: var(--text-primary) !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: var(--bg-secondary);
        border-right: 1px solid var(--border-color);
    }

    /* Cards */
    .card {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid var(--border-color);
        color: var(--text-primary);
    }

    .card-white {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid var(--border-color);
        color: var(--text-primary);
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    /* Métricas */
    [data-testid="stMetricValue"] {
        color: var(--accent) !important;
    }

    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
    }

    .metric-value {
        font-size: 2.5em;
        font-weight: bold;
        color: var(--accent);
    }

    .metric-label {
        color: var(--text-secondary);
        font-size: 0.9em;
    }

    /* Tabelas */
    .stDataFrame {
        border: 1px solid var(--border-color) !important;
        border-radius: 8px;
    }

    .stDataFrame th {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
    }

    .stDataFrame td {
        color: var(--text-primary) !important;
    }

    /* Botões */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    /* Inputs */
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        background: var(--bg-card);
        border-color: var(--border-color);
        color: var(--text-primary);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-secondary);
    }

    /* ============================================
       BADGES DE STATUS - CORES FIXAS NOS 2 TEMAS
       ============================================ */
    
    /* Badge de SUCESSO (verde) */
    .badge-success {
        background: #238636 !important;
        color: #ffffff !important;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Badge de AVISO (amarelo/laranja) */
    .badge-warning {
        background: #d29922 !important;
        color: #ffffff !important;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Badge de ERRO (vermelho) */
    .badge-error {
        background: #da3633 !important;
        color: #ffffff !important;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
        display: inline-block;
    }
    
    /* ============================================
       INDICADORES DE PONTUAÇÃO NOS CARDS
       ============================================ */
    
    /* Fundo verde claro para acerto de placar */
    .score-exact {
        background: #d4edda !important;
        border-left: 5px solid #28a745 !important;
        color: #155724 !important;
    }
    
    [data-theme="dark"] .score-exact {
        background: #0d3320 !important;
        border-left: 5px solid #3fb950 !important;
        color: #7ee787 !important;
    }
    
    /* Fundo amarelo claro para acerto de resultado */
    .score-result {
        background: #fff3cd !important;
        border-left: 5px solid #ffc107 !important;
        color: #856404 !important;
    }
    
    [data-theme="dark"] .score-result {
        background: #3d2e00 !important;
        border-left: 5px solid #d29922 !important;
        color: #e3b341 !important;
    }
    
    /* Fundo vermelho claro para erro */
    .score-miss {
        background: #f8d7da !important;
        border-left: 5px solid #dc3545 !important;
        color: #721c24 !important;
    }
    
    [data-theme="dark"] .score-miss {
        background: #3d1216 !important;
        border-left: 5px solid #da3633 !important;
        color: #f0888a !important;
    }
    
    /* ============================================
       TEXTO DE PONTUAÇÃO COLORIDO
       ============================================ */
    
    .points-green {
        color: #28a745 !important;
        font-weight: bold;
    }
    
    [data-theme="dark"] .points-green {
        color: #3fb950 !important;
    }
    
    .points-yellow {
        color: #d29922 !important;
        font-weight: bold;
    }
    
    [data-theme="dark"] .points-yellow {
        color: #e3b341 !important;
    }
    
    .points-red {
        color: #dc3545 !important;
        font-weight: bold;
    }
    
    [data-theme="dark"] .points-red {
        color: #da3633 !important;
    }
    /* Título gradiente */
    .title-gradient {
        font-weight: 800;
        color: var(--accent) !important;
        -webkit-text-fill-color: var(--accent) !important;
    }

    /* Divisores */
    hr {
        border-color: var(--border-color) !important;
    }

    /* Links */
    a {
        color: var(--accent) !important;
    }
    /* ============================================
       BARRA DE PROGRESSO
       ============================================ */
    
    /* Fundo da barra - cinza nos dois temas */
    .stProgress > div > div {
        background-color: #d0d7de !important;
    }
    
    [data-theme="dark"] .stProgress > div > div {
        background-color: #30363d !important;
    }
    
    /* ============================================
       MÉTRICAS COM BORDA
       ============================================ */
    
    /* Borda preta no light, branca no dark */
    [data-testid="stMetric"] {
        border: 2px solid #1f2328 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        background: var(--bg-card);
    }
    
    [data-theme="dark"] [data-testid="stMetric"] {
        border: 2px solid #e6edf3 !important;
    }
    
    /* ============================================
       CARDS COM BORDA
       ============================================ */
    
    .card {
        border: 2px solid #1f2328 !important;
    }
    
    [data-theme="dark"] .card {
        border: 2px solid #e6edf3 !important;
    }
    
    .card-white {
        border: 2px solid #1f2328 !important;
    }
    
    [data-theme="dark"] .card-white {
        border: 2px solid #e6edf3 !important;
    }
    
    /* ============================================
       AVATARES COM BORDA
       ============================================ */
    
    .avatar-img {
        border: 3px solid #1f2328 !important;
    }
    
    [data-theme="dark"] .avatar-img {
        border: 3px solid #e6edf3 !important;
    }
    
    /* ============================================
       BANDEIRAS COM BORDA
       ============================================ */
    
    .flag-img {
        border: 1px solid #1f2328 !important;
    }
    
    [data-theme="dark"] .flag-img {
        border: 1px solid #e6edf3 !important;
    }
    
    /* ============================================
       TABELAS COM BORDA
       ============================================ */
    
    .stDataFrame {
        border: 2px solid #1f2328 !important;
    }
    
    [data-theme="dark"] .stDataFrame {
        border: 2px solid #e6edf3 !important;
    }
    
    /* ============================================
       INPUTS COM BORDA
       ============================================ */
    
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        border: 2px solid #1f2328 !important;
    }
    
    [data-theme="dark"] .stSelectbox > div > div,
    [data-theme="dark"] .stNumberInput > div > div > input {
        border: 2px solid #e6edf3 !important;
    }
</style>
""", unsafe_allow_html=True)
# ============================================
# INICIALIZAÇÃO
# ============================================
@st.cache_resource
def init_managers():
    """Inicializa os gerenciadores (cacheado)"""
    return {
        'assets': AssetsManager(),
        'results': ManualResultsManager(),
        'engine': ScoringEngine(),
        'processor': PredictionProcessor()
    }


managers = init_managers()
assets = managers['assets']
results_manager = managers['results']
engine = managers['engine']
processor = managers['processor']


# ============================================
# CARREGAR DADOS
# ============================================
@st.cache_data(ttl=60)
def load_data():
    """Carrega todos os dados"""
    # Previsões
    predictions = processor.consolidate_predictions()

    # Resultados reais
    real_results = results_manager.get_only_completed_results()

    # Pontuação
    scored = pd.DataFrame()
    leaderboard = pd.DataFrame()

    if not predictions.empty and not real_results.empty:
        scored = engine.calculate_scores(predictions, real_results)
        if not scored.empty:
            leaderboard = engine.get_leaderboard(scored)

    return predictions, real_results, scored, leaderboard


predictions, real_results, scored, leaderboard = load_data()

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("## ⚽ Bolão Copa do Mundo 2026")
    st.markdown("---")

    # Menu
    pagina = st.radio(
        "📋 Navegação",
        ["🏠 Visão Geral", "🏆 Ranking", "📊 Grupos", "🎯 Palpites", "📝 Resultados"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Estatísticas rápidas
    st.markdown("### 📊 Resumo")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Jogos", f"{len(real_results)}/72")
    with col2:
        st.metric("Competidores", f"{len(leaderboard)}")

    st.markdown("---")

    # Competidores ativos
    if not leaderboard.empty:
        st.markdown("### 👥 Participantes")
        for _, row in leaderboard.iterrows():
            info = assets.get_competitor_info(row['competidor'])
            avatar_html = assets.get_avatar_html(row['competidor'], 30)
            st.markdown(
                f"{avatar_html} **{row['competidor']}** - {int(row['pontos_total'])} pts",
                unsafe_allow_html=True
            )

# ============================================
# PÁGINA: VISÃO GERAL
# ============================================
if pagina == "🏠 Visão Geral":
    st.markdown('<h1 class="title-gradient">🏆 Copa do Mundo 2026</h1>', unsafe_allow_html=True)
    st.markdown("### 🇨🇦 Canadá • 🇲🇽 México • 🇺🇸 Estados Unidos")

    # Cards de estatísticas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <div class="metric-label">Jogos Realizados</div>
            <div class="metric-value">{}</div>
            <div class="metric-label">de 72</div>
        </div>
        """.format(len(real_results)), unsafe_allow_html=True)

    with col2:
        total_palpites = len(predictions) if not predictions.empty else 0
        st.markdown("""
        <div class="card" style="text-align: center;">
            <div class="metric-label">Palpites</div>
            <div class="metric-value">{}</div>
            <div class="metric-label">registrados</div>
        </div>
        """.format(total_palpites), unsafe_allow_html=True)

    with col3:
        lider_nome = leaderboard.iloc[0]['competidor'] if not leaderboard.empty else "-"
        lider_pts = int(leaderboard.iloc[0]['pontos_total']) if not leaderboard.empty else 0
        st.markdown("""
        <div class="card" style="text-align: center;">
            <div class="metric-label">🥇 Líder</div>
            <div class="metric-value">{}</div>
            <div class="metric-label">{} pts</div>
        </div>
        """.format(lider_nome, lider_pts), unsafe_allow_html=True)

    with col4:
        progresso = results_manager.get_progress()
        pct = progresso.get('porcentagem', 0)
        st.markdown("""
        <div class="card" style="text-align: center;">
            <div class="metric-label">Progresso</div>
            <div class="metric-value">{}%</div>
            <div class="metric-label">da Copa</div>
        </div>
        """.format(pct), unsafe_allow_html=True)

    st.markdown("---")

    # Ranking rápido (Top 5)
    if not leaderboard.empty:
        st.markdown("### 🏆 Top 5")

        cols = st.columns(5)
        medals = ['🥇', '🥈', '🥉', '4º', '5º']

        for i, (_, row) in enumerate(leaderboard.head(5).iterrows()):
            with cols[i]:
                info = assets.get_competitor_info(row['competidor'])
                avatar_html = assets.get_avatar_html(row['competidor'], 60)

                st.markdown(f"""
                <div class="card" style="text-align: center;">
                    <div style="font-size: 2em;">{medals[i]}</div>
                    {avatar_html}
                    <div style="margin-top: 10px; font-weight: bold;">{row['competidor']}</div>
                    <div style="font-size: 1.5em; color: #FFD700;">{int(row['pontos_total'])}</div>
                    <div style="font-size: 0.8em; color: #999;">pontos</div>
                </div>
                """, unsafe_allow_html=True)

    # Gráfico de barras
    if not leaderboard.empty:
        st.markdown("---")
        st.markdown("### 📊 Pontuação por Competidor")

        fig = px.bar(
            leaderboard,
            x='competidor',
            y='pontos_total',
            color='placares_exatos',
            title='',
            labels={
                'pontos_total': 'Pontos',
                'placares_exatos': 'Placares Exatos',
                'competidor': ''
            },
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# PÁGINA: RANKING
# ============================================
elif pagina == "🏆 Ranking":
    st.markdown('<h1 class="title-gradient">🏆 Classificação Completa</h1>', unsafe_allow_html=True)

    if leaderboard.empty:
        st.warning("⚠️ Nenhum dado disponível. Cadastre resultados primeiro!")
    else:
        # Cards do pódio
        col1, col2, col3 = st.columns([1, 1.5, 1])

        # 2º lugar
        if len(leaderboard) > 1:
            with col1:
                row = leaderboard.iloc[1]
                info = assets.get_competitor_info(row['competidor'])
                st.markdown(f"""
                <div class="card" style="text-align: center; margin-top: 40px;">
                    <div style="font-size: 3em;">🥈</div>
                    {assets.get_avatar_html(row['competidor'], 70)}
                    <h3>{row['competidor']}</h3>
                    <div style="font-size: 2em; color: #C0C0C0;">{int(row['pontos_total'])}</div>
                    <small>pts</small>
                </div>
                """, unsafe_allow_html=True)

        # 1º lugar
        if len(leaderboard) > 0:
            with col2:
                row = leaderboard.iloc[0]
                info = assets.get_competitor_info(row['competidor'])
                st.markdown(f"""
                <div class="card" style="text-align: center; border: 2px solid #FFD700;">
                    <div style="font-size: 4em;">🥇</div>
                    {assets.get_avatar_html(row['competidor'], 90)}
                    <h2>{row['competidor']}</h2>
                    <div style="font-size: 2.5em; color: #FFD700;">{int(row['pontos_total'])}</div>
                    <small>pts</small>
                    <div style="margin-top: 10px;">
                        <span class="badge-success">🎯 {int(row['placares_exatos'])} placares</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # 3º lugar
        if len(leaderboard) > 2:
            with col3:
                row = leaderboard.iloc[2]
                info = assets.get_competitor_info(row['competidor'])
                st.markdown(f"""
                <div class="card" style="text-align: center; margin-top: 40px;">
                    <div style="font-size: 3em;">🥉</div>
                    {assets.get_avatar_html(row['competidor'], 70)}
                    <h3>{row['competidor']}</h3>
                    <div style="font-size: 2em; color: #CD7F32;">{int(row['pontos_total'])}</div>
                    <small>pts</small>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

        # Tabela completa
        st.markdown("### 📋 Tabela Completa")

        display_df = leaderboard.copy()
        display_df['Média'] = display_df['media_pontos'].round(1)
        display_df['Aprov.'] = display_df['aproveitamento'].round(1).astype(str) + '%'

        st.dataframe(
            display_df[[
                'posicao', 'competidor', 'pontos_total', 'placares_exatos',
                'resultados_corretos', 'Média', 'Aprov.'
            ]].rename(columns={
                'posicao': '#',
                'competidor': 'Competidor',
                'pontos_total': 'Pontos',
                'placares_exatos': 'Placar Exato',
                'resultados_corretos': 'Resultados'
            }),
            hide_index=True,
            use_container_width=True,
            column_config={
                '#': st.column_config.NumberColumn(width='small'),
                'Pontos': st.column_config.NumberColumn(width='medium'),
            }
        )

# ============================================
# PÁGINA: GRUPOS
# ============================================
elif pagina == "📊 Grupos":
    st.markdown('<h1 class="title-gradient">📊 Grupos da Copa</h1>', unsafe_allow_html=True)

    # Tabs para cada grupo
    grupos_letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
    tabs = st.tabs([f"Grupo {g}" for g in grupos_letras])

    for i, tab in enumerate(tabs):
        with tab:
            grupo = grupos_letras[i]
            st.markdown(f"### Grupo {grupo}")

            # Busca seleções do grupo
            from copa2026_data import GRUPOS_COPA_2026

            grupo_info = GRUPOS_COPA_2026.get(grupo, {})
            selecoes = grupo_info.get('selecoes', [])

            if selecoes:
                cols = st.columns(4)
                for j, selecao in enumerate(selecoes):
                    with cols[j]:
                        flag_html = assets.get_flag_html(selecao, 60)
                        st.markdown(f"""
                        <div class="card" style="text-align: center;">
                            {flag_html}
                            <div style="margin-top: 10px; font-weight: bold;">{selecao}</div>
                        </div>
                        """, unsafe_allow_html=True)

            # Resultados do grupo
            st.markdown("---")
            st.markdown("#### Resultados")

            grupo_results = results_manager.get_results_by_group(grupo)
            realizados = [r for r in grupo_results if r.get('status') == 'Realizado']

            if realizados:
                for jogo in realizados:
                    placar = f"{jogo.get('placar_casa', '-')} x {jogo.get('placar_visitante', '-')}"
                    st.markdown(
                        f"⚽ {jogo.get('casa')} **{placar}** {jogo.get('visitante')} "
                        f"({jogo.get('data', '')})"
                    )
            else:
                st.info("Nenhum resultado cadastrado ainda.")

# ============================================
# PÁGINA: PALPITES
# ============================================
elif pagina == "🎯 Palpites":
    st.markdown('<h1 class="title-gradient">🎯 Palpites por Jogo</h1>', unsafe_allow_html=True)

    if scored.empty:
        st.warning("Cadastre resultados para ver os palpites!")
    else:
        col1, col2 = st.columns(2)

        with col1:
            lista_comp = ["Todos"] + sorted(list(scored["competidor"].unique()))
            comp_sel = st.selectbox("Competidor", lista_comp)

        with col2:
            lista_jogos = ["Todos os jogos"]

            # Pega jogos únicos com data (para ordenar do mais recente)
            jogos_data = scored[["grupo", "time_casa", "time_visitante", "data_jogo"]].drop_duplicates()
            jogos_data = jogos_data.sort_values("data_jogo", ascending=False)

            for _, r in jogos_data.iterrows():
                lista_jogos.append(f"Grupo {r['grupo']} - {r['time_casa']} vs {r['time_visitante']}")

            jogo_sel = st.selectbox("Jogo", lista_jogos)

        # Filtra
        df = scored.copy()
        if comp_sel != "Todos":
            df = df[df["competidor"] == comp_sel]
        if jogo_sel != "Todos os jogos":
            parte = jogo_sel.split(" - ")[1]
            casa, visitante = parte.split(" vs ")
            df = df[(df["time_casa"] == casa.strip()) & (df["time_visitante"] == visitante.strip())]

        st.write(f"Mostrando {len(df)} de {len(scored)} palpites")

        if df.empty:
            st.warning("Nenhum palpite encontrado!")
        else:
            for _, row in df.iterrows():
                pts = int(row["pontos"])

                if row["acertou_placar"]:
                    bg = "#06aa48"
                    border = "#28a745"
                    color_text = "#155724"
                    color_badge = "#2da44e"
                    icon = "🎯"
                    txt = "PLACAR EXATO!"
                elif row["acertou_resultado"]:
                    bg = "#ffab00"
                    border = "#d29922"
                    color_text = "#856404"
                    color_badge = "#bf8700"
                    icon = "✓"
                    txt = "ACERTOU RESULTADO"
                else:
                    bg = "#ff3344"
                    border = "#dc3545"
                    color_text = "#721c24"
                    color_badge = "#e5534b"
                    icon = "✗"
                    txt = "ERROU"

                flag1 = assets.get_flag_html(row["time_casa"], 30)
                flag2 = assets.get_flag_html(row["time_visitante"], 30)

                html = (
                        '<div style="background:' + bg + ';border-left:5px solid ' + border + ';'
                                                                                              'border-radius:12px;padding:16px;margin:8px 0;">'

                # Times e placar centralizados
                                                                                              '<div style="display:flex;align-items:center;justify-content:center;gap:20px;text-align:center;">'
                                                                                              '<div style="flex:1;text-align:center;">' + flag1 + '<br><b>' + str(
                    row["time_casa"]) + '</b></div>'
                                        '<div style="flex:1;text-align:center;font-size:1.3em;">'
                                        '<span>' + str(row["placar_previsto"]) + '</span>'
                                                                                 '<span style="margin:0 10px;color:#666;">vs</span>'
                                                                                 '<b style="font-size:1.1em;">' + str(
                    row["placar_real"]) + '</b>'
                                          '</div>'
                                          '<div style="flex:1;text-align:center;">' + flag2 + '<br><b>' + str(
                    row["time_visitante"]) + '</b></div>'
                                             '</div>'

                        # Status e pontuação
                                             '<div style="text-align:center;margin-top:12px;padding-top:10px;border-top:1px solid rgba(0,0,0,0.1);">'
                                             '<span style="background:' + color_badge + ';color:white;padding:4px 14px;border-radius:20px;font-weight:bold;font-size:0.95em;">'
                        + icon + ' ' + txt +
                        '</span>'
                        '<span style="margin-left:12px;font-weight:bold;font-size:1.1em;color:' + color_text + ';">'
                        + str(pts) + ' pts</span>'
                                     '<span style="margin-left:12px;color:' + color_text + ';">' +
assets.get_avatar_html(str(row["competidor"]), 24) +
' <b>' + str(row["competidor"]) + '</b></span>'
                                         '</div>'
                                         '</div>'
                )

                st.markdown(html, unsafe_allow_html=True)
# ============================================
# PÁGINA: RESULTADOS
# ============================================
elif pagina == "📝 Resultados":
    st.markdown('<h1 class="title-gradient">📝 Cadastrar Resultados</h1>', unsafe_allow_html=True)

    # Progresso
    progress = results_manager.get_progress()
    pct = progress.get('porcentagem', 0)

    st.markdown(f"""
    <div class="card" style="text-align: center;">
        <h3>Progresso: {pct}%</h3>
        <div style="background: rgba(255,255,255,0.2); height: 20px; border-radius: 10px;">
            <div style="background: #4CAF50; width: {pct}%; height: 100%; border-radius: 10px;"></div>
        </div>
        <small>{progress.get('jogos_realizados', 0)} de {progress.get('total_jogos', 72)} jogos cadastrados</small>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Selecionar grupo
    grupo = st.selectbox("Filtrar por Grupo", ['Todos'] + [f'Grupo {g}' for g in 'ABCDEFGHIJKL'])

    if grupo != 'Todos':
        letra = grupo.split()[-1]
        jogos_grupo = results_manager.get_results_by_group(letra)
    else:
        jogos_grupo = [
            {**result, 'match_id': match_id}
            for match_id, result in results_manager.results.items()
        ]

    # Mostra jogos para cadastrar
    st.markdown("### Jogos")

    for jogo in jogos_grupo:
        match_id = jogo.get('match_id', '')
        status = jogo.get('status', 'Pendente')

        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])

        with col1:
            flag_casa = assets.get_flag_html(jogo.get('casa', ''), 20)
            flag_visitante = assets.get_flag_html(jogo.get('visitante', ''), 20)
            st.markdown(
                f"{flag_casa} **{jogo.get('casa')}** vs **{jogo.get('visitante')}** {flag_visitante}",
                unsafe_allow_html=True
            )
            st.caption(f"{jogo.get('data', '')} • {jogo.get('cidade', '')}")

        with col2:
            placar_casa = st.number_input(
                "Casa", min_value=0, max_value=15,
                value=jogo.get('placar_casa') or 0,
                key=f"casa_{match_id}"
            )

        with col3:
            st.markdown("<div style='text-align: center; padding-top: 25px;'>x</div>",
                        unsafe_allow_html=True)

        with col4:
            placar_visitante = st.number_input(
                "Fora", min_value=0, max_value=15,
                value=jogo.get('placar_visitante') or 0,
                key=f"fora_{match_id}"
            )

        with col5:
            st.markdown("<div style='padding-top: 20px;'>", unsafe_allow_html=True)

            if st.button("💾 Salvar", key=f"save_{match_id}"):
                results_manager.update_result(match_id, int(placar_casa), int(placar_visitante))
                st.success("✅ Salvo!")
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# RODAPÉ
# ============================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: rgba(255,255,255,0.5); font-size: 0.8em;'>"
    "🏆 Bolão Copa do Mundo 2026 • Desenvolvido por Anderson Silva"
    "</div>",
    unsafe_allow_html=True
)