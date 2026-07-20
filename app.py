import streamlit as st
import pandas as pd
import plotly.express as px
import os
import requests
from datetime import datetime, timedelta

# Configuração da Página
st.set_page_config(page_title="SISTER | Resiliência Climática", layout="wide", page_icon="🌧️")

# Injeção de CSS Customizado para identidade do SISTER
custom_css = """
<style>
/* Fundo principal e fontes globais gerenciadas pelo config.toml */

/* Customização dos Cards de Métricas (stMetric) */
[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 15px 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    border-top: 3px solid #2ea8e8;
}
[data-testid="stMetricLabel"] {
    font-size: 0.85rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
[data-testid="stMetricValue"] {
    font-size: 1.8rem;
    font-weight: 800;
    color: #0f172a;
}

/* Títulos do Topbar */
.main-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #0c2844;
    margin-bottom: -10px;
}
.sub-title {
    font-size: 1rem;
    color: #64748b;
    margin-bottom: 20px;
}

/* Abas */
.stTabs [data-baseweb="tab-list"] {
    gap: 20px;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    white-space: pre-wrap;
    background-color: transparent;
    border-radius: 4px 4px 0px 0px;
    gap: 1px;
    padding-top: 10px;
    padding-bottom: 10px;
    color: #64748b;
}
.stTabs [aria-selected="true"] {
    color: #0c2844 !important;
    font-weight: 700 !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown('<div class="main-title">🌧️ SISTER | Painel de Resiliência Climática</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Monitoramento Analítico de Precipitação via Open-Meteo API</div>', unsafe_allow_html=True)

# ---- Carregar Dados do IBGE via GitHub ----
@st.cache_data(ttl=24*3600)
def load_estados():
    url = "https://raw.githubusercontent.com/kelvins/Municipios-Brasileiros/main/csv/estados.csv"
    df = pd.read_csv(url)
    return df

@st.cache_data(ttl=24*3600)
def load_municipios():
    url = "https://raw.githubusercontent.com/kelvins/Municipios-Brasileiros/main/csv/municipios.csv"
    df = pd.read_csv(url)
    return df

df_estados = load_estados()
df_municipios = load_municipios()

tab1, tab2 = st.tabs(["🌎 Explorador Nacional (Tempo Real)", "📊 Operação Consolidada (RS)"])

# ==========================================
# ABA 1: Explorador Nacional
# ==========================================
with tab1:
    st.markdown("### Selecione a Região de Análise")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        lista_estados = df_estados.sort_values("nome")
        estado_sel_nome = st.selectbox("Estado (UF):", lista_estados["nome"])
        
    with col2:
        uf_id = lista_estados[lista_estados["nome"] == estado_sel_nome]["codigo_uf"].values[0]
        lista_municipios = df_municipios[df_municipios["codigo_uf"] == uf_id].sort_values("nome")
        municipio_sel_nome = st.selectbox("Município:", lista_municipios["nome"])
        
    with col3:
        st.write("")
        st.write("")
        buscar = st.button("Gerar Relatório (Últimos 30 dias)", type="primary", use_container_width=True)

    if buscar:
        cidade_info = lista_municipios[lista_municipios["nome"] == municipio_sel_nome].iloc[0]
        lat, lon = cidade_info["latitude"], cidade_info["longitude"]

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat, "longitude": lon,
            "daily": "precipitation_sum", "timezone": "America/Sao_Paulo",
            "start_date": start_date, "end_date": end_date
        }

        try:
            res = requests.get(url, params=params, timeout=15)
            res.raise_for_status()
            data = res.json()
            
            df_live = pd.DataFrame({
                "Data": data["daily"]["time"], 
                "Chuva (mm)": data["daily"]["precipitation_sum"]
            })
            df_live["Data"] = pd.to_datetime(df_live["Data"])
            df_live["Chuva (mm)"] = df_live["Chuva (mm)"].fillna(0.0)
            df_live["Acumulado (mm)"] = df_live["Chuva (mm)"].cumsum()
            
            def categorizar_chuva(mm):
                if mm < 1: return "Sem Chuva"
                elif mm < 10: return "Leve (1-10mm)"
                elif mm < 25: return "Moderada (10-25mm)"
                else: return "Forte (>25mm)"
                
            df_live["Intensidade"] = df_live["Chuva (mm)"].apply(categorizar_chuva)

            st.divider()
            st.markdown(f"### Painel de Diagnóstico: **{municipio_sel_nome} - {estado_sel_nome}**")
            
            # --- ROW 1: CARDS (KPIs) ---
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            kpi1.metric("Volume Acumulado", f"{df_live['Chuva (mm)'].sum():.1f} mm")
            kpi2.metric("Chuva Máxima (Dia)", f"{df_live['Chuva (mm)'].max():.1f} mm")
            kpi3.metric("Média Diária", f"{df_live['Chuva (mm)'].mean():.1f} mm")
            kpi4.metric("Dias Chuvosos (>1mm)", f"{(df_live['Chuva (mm)'] >= 1).sum()}")
            
            st.write("")
            
            # --- ROW 2: GRAFICOS TEMPORAIS ---
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                fig1 = px.bar(
                    df_live, x="Data", y="Chuva (mm)", 
                    title="Distribuição Diária de Precipitação",
                    template="plotly_white",
                    color_discrete_sequence=["#2ea8e8"]
                )
                fig1.update_layout(margin=dict(l=20, r=20, t=40, b=20), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig1, use_container_width=True)
                
            with col_chart2:
                fig2 = px.line(
                    df_live, x="Data", y="Acumulado (mm)", 
                    title="Curva de Acúmulo Mensal",
                    template="plotly_white",
                    color_discrete_sequence=["#f59e0b"]
                )
                fig2.update_traces(fill='tozeroy', fillcolor="rgba(245, 158, 11, 0.1)")
                fig2.update_layout(margin=dict(l=20, r=20, t=40, b=20), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig2, use_container_width=True)

            # --- ROW 3: DONUT & TABLE ---
            col_donut, col_table = st.columns([1, 1.5])
            with col_donut:
                contagem = df_live["Intensidade"].value_counts().reset_index()
                contagem.columns = ["Intensidade", "Dias"]
                cores_map = {"Sem Chuva": "#e2e8f0", "Leve (1-10mm)": "#7dd3fc", "Moderada (10-25mm)": "#2ea8e8", "Forte (>25mm)": "#0c2844"}
                
                fig3 = px.pie(
                    contagem, values="Dias", names="Intensidade", hole=0.6,
                    title="Classificação de Eventos",
                    color="Intensidade", color_discrete_map=cores_map
                )
                fig3.update_layout(margin=dict(l=0, r=0, t=40, b=0), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", showlegend=True, legend=dict(orientation="h", y=-0.1))
                st.plotly_chart(fig3, use_container_width=True)
                
            with col_table:
                st.markdown("**Registro Analítico Diário**")
                st.dataframe(
                    df_live.sort_values(by="Data", ascending=False).style.format({"Chuva (mm)": "{:.1f}", "Acumulado (mm)": "{:.1f}"}),
                    use_container_width=True, height=300
                )
        except Exception as e:
            st.error(f"Erro na comunicação com a API: {e}")

# ==========================================
# ABA 2: Dados Históricos do RS
# ==========================================
with tab2:
    st.markdown("### Controle Base Operacional - Rio Grande do Sul")
    st.markdown("Gestão dos dados salvos no repositório pela rotina de automação `daily_fetch`.")
    
    CSV_PATH = "data/chuva_diaria.csv"
    if not os.path.exists(CSV_PATH):
        st.warning("Nenhum arquivo 'chuva_diaria.csv' encontrado. Aguarde a automação ou execute o script de coleta.")
    else:
        df = pd.read_csv(CSV_PATH)
        df["data"] = pd.to_datetime(df["data"])

        cidades_sel = st.multiselect("Cidades Ativas:", options=sorted(df["cidade"].unique()), default=df["cidade"].unique())
        datas_disponiveis = df["data"].dt.date.unique()
        
        if len(datas_disponiveis) > 0:
            datas_selecionadas = st.date_input("Filtro de Período:", value=(min(datas_disponiveis), max(datas_disponiveis)), min_value=min(datas_disponiveis), max_value=max(datas_disponiveis))
            
            if isinstance(datas_selecionadas, tuple) and len(datas_selecionadas) == 2:
                data_inicio, data_fim = datas_selecionadas
            else:
                data_inicio = data_fim = datas_selecionadas[0] if isinstance(datas_selecionadas, tuple) else datas_selecionadas

            mask = (df["cidade"].isin(cidades_sel)) & (df["data"].dt.date >= data_inicio) & (df["data"].dt.date <= data_fim)
            df_filtrado = df[mask]

            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric("Soma Total no Período", f"{df_filtrado['precipitacao_mm'].sum():.1f} mm")
            kpi2.metric("Média de Precipitação", f"{df_filtrado['precipitacao_mm'].mean():.1f} mm")
            kpi3.metric("Maior Evento Crítico", f"{df_filtrado['precipitacao_mm'].max():.1f} mm")

            st.write("")
            col_chart, col_map = st.columns(2)
            with col_chart:
                fig_linha = px.line(df_filtrado, x="data", y="precipitacao_mm", color="cidade", title="Evolução Temporal Comparativa", template="plotly_white")
                fig_linha.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_linha, use_container_width=True)

            with col_map:
                try:
                    fig_mapa = px.scatter_map(
                        df_filtrado, lat="latitude", lon="longitude", size="precipitacao_mm", color="precipitacao_mm",
                        hover_name="cidade", hover_data=["data", "precipitacao_mm"], color_continuous_scale="Blues",
                        size_max=35, zoom=5.5, title="Mapa de Volume Espacial"
                    )
                except AttributeError:
                    fig_mapa = px.scatter_mapbox(
                        df_filtrado, lat="latitude", lon="longitude", size="precipitacao_mm", color="precipitacao_mm",
                        hover_name="cidade", hover_data=["data", "precipitacao_mm"], color_continuous_scale="Blues",
                        size_max=35, zoom=5.5, title="Mapa de Volume Espacial", mapbox_style="open-street-map"
                    )
                fig_mapa.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_mapa, use_container_width=True)
