# 🌧️ SISTER | Painel de Resiliência Climática

Bem-vindo ao repositório do **SISTER | Painel de Resiliência Climática**! Este projeto é uma solução completa em Python para coletar, armazenar e visualizar dados de precipitação (chuva) utilizando a API gratuita do [Open-Meteo](https://open-meteo.com/).

O projeto é dividido em dois grandes pilares:
1. **Automação de Coleta (GitHub Actions)**: Uma rotina diária que consulta a chuva acumulada para os principais municípios do Rio Grande do Sul (RS) e armazena os dados historicamente em um arquivo CSV.
2. **Dashboard Interativo (Streamlit)**: Um painel visual com mapas e gráficos que permite tanto visualizar o histórico coletado do RS quanto explorar dinamicamente a chuva nos últimos 30 dias para **qualquer município do Brasil**.

---

## 🚀 Funcionalidades

### 🌎 Explorador Nacional (Tempo Real)
- Consulta de precipitação (últimos 30 dias) sob demanda para mais de **5.500 municípios brasileiros**.
- Seleção fácil de **Estado (UF) ➔ Município**.
- Gráficos interativos com totais acumulados e picos de chuva.

### 📊 Visão Geral Consolidada (Rio Grande do Sul)
- Base de dados estática atualizada diariamente de forma automática (`data/chuva_diaria.csv`).
- Visualização de evolução temporal por cidade.
- Mapa interativo (bolhas proporcionais ao volume de chuva).

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.11+
- **Bibliotecas**: `pandas`, `requests`, `streamlit`, `plotly`
- **Automação**: GitHub Actions
- **Fontes de Dados**:
  - Clima: [Open-Meteo API](https://open-meteo.com/)
  - Municípios BR: [kelvins/Municipios-Brasileiros](https://github.com/kelvins/Municipios-Brasileiros)

---

## 📂 Estrutura do Repositório

```text
Open-Meteo/
├── .github/
│   └── workflows/
│       └── daily_fetch.yml   # Automação do GitHub Actions (roda às 06:00 UTC)
├── data/
│   └── chuva_diaria.csv      # Base de dados acumulada do RS
├── app.py                    # Dashboard Streamlit
├── coletor.py                # Script Python de extração de dados (RS)
├── requirements.txt          # Dependências do projeto
└── LICENSE                   # Licença GNU GPLv3
```

---

## 💻 Como Rodar Localmente

1. **Clone o repositório:**
   ```bash
   git clone git@github.com:jpereiratrindade/Open-Meteo.git
   cd Open-Meteo
   ```

2. **Crie um ambiente virtual e instale as dependências:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Inicie o Dashboard:**
   ```bash
   streamlit run app.py
   ```
   O painel abrirá automaticamente no seu navegador em `http://localhost:8501`.

---

## 🤖 Automação no GitHub Actions

O arquivo `.github/workflows/daily_fetch.yml` garante que o arquivo `coletor.py` seja executado todos os dias. 
**Atenção:** Para que a automação tenha permissão de salvar o arquivo CSV no repositório, certifique-se de que a opção **Read and write permissions** está ativa em:
`Settings > Actions > General > Workflow permissions` no seu repositório do GitHub.

---

## 📄 Licença

Este projeto está sob a licença **GNU GPLv3**. Veja o arquivo `LICENSE` para mais detalhes.
