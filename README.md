# 🏆 Bolão Copa do Mundo 2026

Sistema completo para gerenciar bolão da Copa do Mundo FIFA 2026
- **48 seleções** | **12 grupos** (A-L) | **72 jogos** na fase de grupos
- Sedes: Canadá, México e Estados Unidos
- Data: 11 de junho a 19 de julho de 2026

## 📋 Regras de Pontuação
- Acertou o resultado do jogo (vitória/empate/derrota): **15 pontos**
- Acertou o placar exato: **35 pontos**

## 🚀 Instalação e Uso

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Baixar bandeiras das seleções
```bash
python utils/download_flags.py
```

### 3. Criar template para competidores
```bash
python utils/create_template.py
```

### 4. Coletar palpites
Distribua o template gerado em `planilhas_competidores/` para cada competidor.
Cada um deve salvar como: `NOME_previsoes.xlsx`

### 5. Validar planilhas (opcional)
```bash
python utils/validate_data.py
```

### 6. Executar o dashboard
```bash
streamlit run src/dashboard.py
```
Acesse no navegador: https://bolao-copa-2026-soma-8a.streamlit.app/

### 7. Menu rápido
```bash
python run.py
```

## 📁 Estrutura do Projeto
```
bolao-copa-2026/
├── assets/                    # Bandeiras e avatares
├── planilhas_competidores/    # Planilhas de palpites
├── data/                      # Dados processados
├── src/                       # Código fonte
├── utils/                     # Utilitários
├── requirements.txt          # Dependências
└── run.py                    # Menu principal
```

## 🎯 Funcionalidades
- Dashboard interativo com Streamlit
- Bandeiras oficiais de todas as 48 seleções
- Avatares personalizados para competidores
- Atualização manual de resultados
- Cálculo automático de pontuação
- Ranking em tempo real
- Gráficos e estatísticas

## 📊 Tecnologias
- Python 3.10+
- Streamlit (Dashboard)
- Pandas (Processamento de dados)
- Plotly (Gráficos)
- Pillow (Imagens)
