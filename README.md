# 🌧️ SISTER-Clima | Painel de Resiliência Climática

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)](https://streamlit.io/)
[![Versão](https://img.shields.io/badge/versão-v2.3-brightgreen)](https://github.com/jpereiratrindade/Open-Meteo/releases/tag/v2.3)
[![Open-Meteo](https://img.shields.io/badge/dados-Open--Meteo%20API-orange)](https://open-meteo.com/)
[![NASA POWER](https://img.shields.io/badge/dados-NASA%20POWER-blue)](https://power.larc.nasa.gov/)
[![Embrapa](https://img.shields.io/badge/Embrapa-Projeto%20Resili%C3%AAncia-green)](https://www.embrapa.br/)

**SISTER-Clima** é o módulo de monitoramento e análise de precipitação pluviométrica do ecossistema **SISTER** (Sistema Integrado de Suporte à Transição e Resiliência) do **Projeto Resiliência – Embrapa**.

> ⚠️ **Nota sobre os dados:** Este sistema trabalha nativamente com duas fontes de dados climáticos distintas (NASA POWER e Open-Meteo), oferecendo tanto **saídas de modelos numéricos de tempo (NWP)** quanto **reanálises históricas (MERRA-2 e ERA5)**.
>
> Os valores exibidos **não representam observações diretas de estações pluviométricas (pluviômetros)**. São aproximações computacionais baseadas em satélites e assimilação de dados globais. Leia atentamente a seção de [Transparência de Dados](#-transparência-de-dados-e-fontes) para recomendações científicas de uso.

---

## ✨ Funcionalidades v2.3

### 🌎 Explorador Nacional
- Seleção dinâmica de **Estado → Município** (5.570 municípios via IBGE)
- Consulta automática dos **últimos 30 dias** com opção de dual data source: **Open-Meteo NWP** ou **NASA POWER MERRA-2**
- KPIs operacionais: volume acumulado, pico máximo, média diária, dias chuvosos
- Gráfico de barras da distribuição diária
- Curva de acúmulo mensal com área preenchida e marcadores
- Rosca de classificação de intensidade de eventos
- Tabela analítica com registro diário ordenável

### 📊 Operação Consolidada (RS)
- Base histórica persistida em `data/chuva_diaria.csv` via **GitHub Actions** (ERA5 Reanalysis)
- Seletor de período flexível: Atalhos (7, 30, 90, 365 dias) ou calendário personalizado
- **Adição de municípios extras** em tempo real via Open-Meteo Archive, plotados lado-a-lado com os dados locais
- Gráfico de linha comparativo multi-cidade com marcadores
- Mapa geoespacial de volume precipitado
- KPIs consolidados do período selecionado

### 🎨 Interface e Governança SISTER
- Topbar com logo SISTER, assinatura **SISTER-Clima** e links
- Barra lateral com navegação, aviso de fontes de dados e **timestamp de última coleta** com base na última entrada do banco local
- Aba exclusiva de **📖 Sobre os Dados** contendo painel de conformidade, tabela comparativa de fontes e roadmap técnico.

---

## 🔬 Transparência de Dados e Fontes

O SISTER-Clima possui integração ativa com duas das maiores bases globais de dados atmosféricos. Devido à natureza computacional dos dados (modelos globais), **é comum e esperado que haja forte discrepância entre os valores reportados por cada modelo** para um mesmo dia e local.

Entenda as razões científicas e as recomendações de uso para cada fonte:

### 🚀 NASA POWER (MERRA-2)
A [NASA POWER API](https://power.larc.nasa.gov/) é baseada na reanálise climática MERRA-2.
- **Tipo:** Reanálise climática (olha para o passado assimilando satélites e estações reais).
- **Resolução Espacial:** Aproximadamente **50 x 50 km** (pixels grandes).
- **Licença:** Domínio público, **uso irrestrito comercial e institucional**. Sem chave de API.
- **Comportamento da Precipitação (`PRECTOTCORR`):** Por ter uma grade muito ampla, o MERRA-2 tira uma grande média espacial da região, o que **"achata" os picos extremos** de tempestades isoladas, mas é mais preciso na soma de grandes períodos e extensões.
- **✅ Recomendação SISTER:** **Agroclimatologia e Hidrologia em Larga Escala.** Ideal para calcular balanço hídrico de bacias hidrográficas inteiras ou verificar anomalias mensais.

### 🟡 Open-Meteo (NWP e ERA5)
O [Open-Meteo](https://open-meteo.com/) é um agregador que fornece saídas diretas de modelos de altíssima resolução (NWP).
- **Tipo:** Modelo Numérico de Tempo (Previsão de curto prazo).
- **Resolução Espacial:** Pode chegar a pixels de **7 x 7 km** (como o modelo ICON-DWD).
- **Licença:** Uso **estritamente pessoal e não-comercial** no modo gratuito.
- **Comportamento da Precipitação:** Devido à alta resolução, consegue captar "células de tempestade" isoladas (ex: choveu 40mm num bairro e nada no outro). Como mostra saídas de previsão (forecast), tende a superestimar picos se comparado com o que realmente caiu.
- **✅ Recomendação SISTER:** **Alertas de Defesa Civil e Eventos Extremos.** Ideal para procurar se houve "risco de tempestade extrema pontual" num dia específico.

| Fonte | API Endpoint | Tipo | Resolução | Uso Comercial |
|---|---|---|---|---|
| **NASA POWER** | `power.larc.nasa.gov` | MERRA-2 Reanalysis | ~50 km | ✅ Livre |
| **Open-Meteo** | `/v1/forecast` | Modelos NWP (ICON/GFS) | ~7 a 11 km | ❌ Restrito |
| **Open-Meteo** | `/v1/archive` | ERA5 ECMWF Reanalysis | ~31 km | ❌ Restrito |
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

*© 2026 Embrapa – SISTER-Clima v2.3*
