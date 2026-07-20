# 🌧️ SISTER | Painel de Resiliência Climática

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)](https://streamlit.io/)
[![Versão](https://img.shields.io/badge/versão-v2.0-brightgreen)](https://github.com/jpereiratrindade/Open-Meteo/releases/tag/v2.0)
[![Open-Meteo API](https://img.shields.io/badge/API-Open--Meteo-orange)](https://open-meteo.com/)
[![Embrapa](https://img.shields.io/badge/Embrapa-Projeto%20Resili%C3%AAncia-green)](https://www.embrapa.br/)

Painel interativo de monitoramento e análise de precipitação pluviométrica, desenvolvido como componente do ecossistema **SISTER** (Sistema Integrado de Suporte à Transição e Resiliência) do Projeto Resiliência – Embrapa.

Integra dados climáticos em tempo real via **Open-Meteo API**, histórico automatizado de municípios estratégicos do Rio Grande do Sul, e exploração ad-hoc nacional via base de municípios do IBGE.

---

## ✨ Funcionalidades v2.0

### 🌎 Explorador Nacional
- Seleção dinâmica de **Estado → Município** (5.570 municípios via IBGE)
- Consulta automática dos **últimos 30 dias** de precipitação diária via Open-Meteo API
- Cards de KPIs operacionais: volume acumulado, pico máximo, média diária, dias chuvosos
- Gráfico de barras da distribuição diária
- Curva de acúmulo mensal com área preenchida e marcadores de ponto
- Rosca de classificação de intensidade (sem chuva / leve / moderada / forte)
- Tabela analítica com registro diário ordenável

### 📊 Operação Consolidada (RS)
- Base histórica persistida em `data/chuva_diaria.csv`, atualizada diariamente via **GitHub Actions**
- Filtro de período e seleção de cidades monitoradas
- **Adição de municípios extras** de qualquer Estado em tempo real, via Open-Meteo Archive API
- Gráfico de linha comparativo multi-cidade com marcadores
- Mapa de bolhas geoespacial com intensidade por volume
- KPIs consolidados do período

### 🎨 Interface SISTER v2.0
- Topbar horizontal fixa com **logo geométrico oficial do SISTER**, assinatura "Resiliência Climática" e acesso rápido ao repositório
- Barra lateral em azul marinho com navegação por seções e rodapé institucional
- Tema claro corporativo com cards de métricas, sombras e bordas superiores em azul SISTER
- Totalmente responsivo

---

## 📁 Estrutura do Repositório

```text
Open-Meteo/
├── .github/
│   └── workflows/
│       └── daily_fetch.yml   # Automação GitHub Actions (06:00 UTC)
├── .streamlit/
│   └── config.toml           # Tema e configurações do Streamlit
├── data/
│   └── chuva_diaria.csv      # Base histórica acumulada (RS)
├── .gitignore
├── LICENSE                   # GNU GPLv3
├── README.md
├── app.py                    # Dashboard Streamlit (interface principal)
├── coletor.py                # Script de extração de dados Open-Meteo
└── requirements.txt          # Dependências Python
```

---

## 🚀 Como Executar Localmente

### Pré-requisitos
- Python 3.10+
- pip

### Instalação

```bash
git clone https://github.com/jpereiratrindade/Open-Meteo.git
cd Open-Meteo
python -m venv venv
source venv/bin/activate      # Linux/macOS
pip install -r requirements.txt
```

### Execução

```bash
streamlit run app.py
```

Acesse em: [http://localhost:8501](http://localhost:8501)

---

## ⚙️ Coleta Automática de Dados (GitHub Actions)

O workflow `.github/workflows/daily_fetch.yml` executa o `coletor.py` diariamente às **06:00 UTC**, atualizando de forma incremental o arquivo `data/chuva_diaria.csv` com os dados de precipitação dos municípios monitorados no Rio Grande do Sul.

Para adicionar novos municípios ao monitoramento automático, edite o dicionário `MUNICIPIOS_RS` no arquivo `coletor.py`.

---

## 📦 Dependências

```
requests
pandas
streamlit
plotly
```

---

## 🏛️ Contexto Institucional

Este painel é parte integrante do **Projeto Resiliência** da Embrapa, dentro do ecossistema **SISTER** (Sistema Integrado de Suporte à Transição e Resiliência), que visa prover ferramentas de monitoramento e governança ambiental baseadas em dados abertos.

---

## 📄 Licença

Este projeto está licenciado sob a **GNU General Public License v3.0**.
Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---

*© 2026 Embrapa – Painel de Resiliência Climática v2.0*
