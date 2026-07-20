# 🌧️ SISTER-Clima | Painel de Resiliência Climática

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)](https://streamlit.io/)
[![Versão](https://img.shields.io/badge/versão-v2.1-brightgreen)](https://github.com/jpereiratrindade/Open-Meteo/releases/tag/v2.1)
[![Open-Meteo](https://img.shields.io/badge/dados-Open--Meteo%20API-orange)](https://open-meteo.com/)
[![Embrapa](https://img.shields.io/badge/Embrapa-Projeto%20Resili%C3%AAncia-green)](https://www.embrapa.br/)

**SISTER-Clima** é o módulo de monitoramento e análise de precipitação pluviométrica do ecossistema **SISTER** (Sistema Integrado de Suporte à Transição e Resiliência) do **Projeto Resiliência – Embrapa**.

> ⚠️ **Nota sobre os dados:** Este sistema utiliza a [Open-Meteo API](https://open-meteo.com/) como fonte de dados climáticos — uma API gratuita e de código aberto que fornece:
> - **`/v1/forecast`** — saída de modelos numéricos de tempo (NWP), usada no Explorador Nacional
> - **`/v1/archive` (ERA5)** — reanálise climática ECMWF, usada na Operação Consolidada RS
>
> Os valores **não representam observações diretas de estações pluviométricas**. São estimativas de modelo (NWP) ou reanálise (ERA5), adequadas para monitoramento operacional e análise climatológica, mas não substituem dados de redes de estações como INMET ou ANA para estudos hidrológicos de precisão.

---

## ✨ Funcionalidades v2.1

### 🌎 Explorador Nacional
- Seleção dinâmica de **Estado → Município** (5.570 municípios via IBGE)
- Consulta automática dos **últimos 30 dias** de precipitação via Open-Meteo NWP
- KPIs operacionais: volume acumulado, pico máximo, média diária, dias chuvosos
- Gráfico de barras da distribuição diária
- Curva de acúmulo mensal com área preenchida e marcadores
- Rosca de classificação de intensidade de eventos
- Tabela analítica com registro diário ordenável

### 📊 Operação Consolidada (RS)
- Base histórica persistida em `data/chuva_diaria.csv` via **GitHub Actions** (ERA5)
- Filtro de período e seleção de cidades monitoradas
- **Adição de municípios extras** de qualquer Estado em tempo real (Open-Meteo Archive)
- Gráfico de linha comparativo multi-cidade com marcadores
- Mapa de bolhas geoespacial
- KPIs consolidados do período

### 🎨 Interface SISTER v2.1
- Topbar com logo SISTER, assinatura **SISTER-Clima**, link direto para Open-Meteo e GitHub
- Barra lateral com navegação, informações de fonte de dados e **timestamp de última atualização**
- Tema corporativo claro com cards de métricas e bordas em azul SISTER
- Nota de clareza científica sobre tipo de dado (NWP vs ERA5)

---

## 🔬 Sobre o Open-Meteo

O [Open-Meteo](https://open-meteo.com/) é uma API meteorológica gratuita e de código aberto que agrega dados de múltiplos modelos numéricos globais (ICON, GFS, ECMWF, etc.) e do arquivo histórico **ERA5 Reanalysis** do ECMWF.

| Endpoint | Tipo | Uso neste sistema |
|---|---|---|
| `/v1/forecast` | Saída de modelo NWP | Explorador Nacional |
| `/v1/archive` (ERA5) | Reanálise ECMWF | Operação Consolidada RS |

Referência: [open-meteo.com/en/docs](https://open-meteo.com/en/docs)

---

## 📁 Estrutura do Repositório

```text
Sister-Clima/           (anteriormente Open-Meteo)
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
├── app.py                    # Dashboard SISTER-Clima (interface principal)
├── coletor.py                # Script de coleta Open-Meteo NWP
└── requirements.txt          # Dependências Python
```

---

## 🚀 Como Executar Localmente

```bash
git clone https://github.com/jpereiratrindade/Sister-Clima.git
cd Sister-Clima
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

> Acesse em: [http://localhost:8501](http://localhost:8501)

---

## ⚙️ Coleta Automática (GitHub Actions)

O workflow executa `coletor.py` diariamente às **06:00 UTC**, atualizando `data/chuva_diaria.csv` com dados NWP do dia anterior para os municípios monitorados no RS. Para adicionar municípios, edite `MUNICIPIOS_RS` em `coletor.py`.

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

Este painel faz parte do **Projeto Resiliência** da Embrapa, ecossistema **SISTER**, voltado ao monitoramento ambiental e governança baseados em dados abertos.

---

## 📄 Licença

GNU General Public License v3.0 — veja [LICENSE](LICENSE).

---

*© 2026 Embrapa – SISTER-Clima v2.1*
