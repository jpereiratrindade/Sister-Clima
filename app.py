import streamlit as st
import pandas as pd
import plotly.express as px
import os
import requests
from datetime import datetime, timedelta

st.set_page_config(page_title="SISTER | Resiliência Climática", layout="wide", page_icon="🌧️")

st.title("🌧️ SISTER | Painel de Resiliência Climática")
st.markdown("Dados de chuva acumulada (mm) via Open-Meteo API.")

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

# Inicializa dados na memória
df_estados = load_estados()
df_municipios = load_municipios()

# Cria as abas principais
tab1, tab2 = st.tabs(["🌎 Explorador Nacional (Ao Vivo)", "📊 Dados Históricos Coletados (RS)"])

# ==========================================
# ABA 1: Explorador Nacional
# ==========================================
with tab1:
    st.header("Consulte Qualquer Município Brasileiro")
    st.markdown("Selecione um estado e município para buscar os dados de precipitação dos últimos 30 dias em tempo real.")

    col1, col2 = st.columns(2)
    with col1:
        lista_estados = df_estados.sort_values("nome")
        estado_sel_nome = st.selectbox("Selecione o Estado:", lista_estados["nome"])
        
    with col2:
        uf_id = lista_estados[lista_estados["nome"] == estado_sel_nome]["codigo_uf"].values[0]
        lista_municipios = df_municipios[df_municipios["codigo_uf"] == uf_id].sort_values("nome")
        municipio_sel_nome = st.selectbox("Selecione o Município:", lista_municipios["nome"])

    if st.button("Buscar Dados (Últimos 30 dias)", type="primary"):
        cidade_info = lista_municipios[lista_municipios["nome"] == municipio_sel_nome].iloc[0]
        lat = cidade_info["latitude"]
        lon = cidade_info["longitude"]

        st.info(f"Buscando dados para {municipio_sel_nome} - {estado_sel_nome} (Lat: {lat}, Lon: {lon})...")
        
        # Faz a chamada para API
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": "precipitation_sum",
            "timezone": "America/Sao_Paulo",
            "start_date": start_date,
            "end_date": end_date
        }

        try:
            res = requests.get(url, params=params, timeout=15)
            res.raise_for_status()
            data = res.json()
            
            datas = data["daily"]["time"]
            precip = data["daily"]["precipitation_sum"]
            
            df_live = pd.DataFrame({"Data": datas, "Precipitação (mm)": precip})
            df_live["Data"] = pd.to_datetime(df_live["Data"])
            df_live["Precipitação (mm)"] = df_live["Precipitação (mm)"].fillna(0.0)

            st.success("Dados carregados com sucesso!")
            
            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("Acumulado nos Últimos 30 Dias", f"{df_live['Precipitação (mm)'].sum():.1f} mm")
            col_m2.metric("Maior Chuva no Período", f"{df_live['Precipitação (mm)'].max():.1f} mm")
            col_m3.metric("Dias com Chuva", f"{(df_live['Precipitação (mm)'] > 0.5).sum()} dias")
            
            # Gráfico de barras
            fig = px.bar(
                df_live, 
                x="Data", 
                y="Precipitação (mm)", 
                title=f"Precipitação Diária em {municipio_sel_nome}", 
                template="plotly_white",
                color_discrete_sequence=["#1f77b4"]
            )
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao buscar os dados na API: {e}")

# ==========================================
# ABA 2: Dados Históricos do RS
# ==========================================
with tab2:
    st.header("Visão Geral Consolidada (Rio Grande do Sul)")
    st.markdown("Base de dados atualizada diariamente pela rotina do GitHub Actions.")
    
    CSV_PATH = "data/chuva_diaria.csv"

    if not os.path.exists(CSV_PATH):
        st.warning("Nenhum dado histórico encontrado ainda. Execute o script `coletor.py` ou aguarde a automação.")
    else:
        df = pd.read_csv(CSV_PATH)
        df["data"] = pd.to_datetime(df["data"])

        # Para abas, é melhor manter os filtros no próprio corpo da aba para não confundir o Explorador
        cidades_sel = st.multiselect(
            "Filtrar Cidades (RS):", 
            options=sorted(df["cidade"].unique()), 
            default=df["cidade"].unique(),
            key="rs_cidades"
        )

        datas_disponiveis = df["data"].dt.date.unique()
        
        if len(datas_disponiveis) > 0:
            datas_selecionadas = st.date_input(
                "Período (RS):",
                value=(min(datas_disponiveis), max(datas_disponiveis)),
                min_value=min(datas_disponiveis),
                max_value=max(datas_disponiveis),
                key="rs_datas"
            )

            # Evita erro se o usuário selecionou apenas uma data
            if isinstance(datas_selecionadas, tuple) and len(datas_selecionadas) == 2:
                data_inicio, data_fim = datas_selecionadas
            else:
                data_inicio = data_fim = datas_selecionadas[0] if isinstance(datas_selecionadas, tuple) else datas_selecionadas

            # Filtrando os dados
            mask = (df["cidade"].isin(cidades_sel)) & (df["data"].dt.date >= data_inicio) & (df["data"].dt.date <= data_fim)
            df_filtrado = df[mask]

            # Métricas Principais
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Acumulado no Período", f"{df_filtrado['precipitacao_mm'].sum():.1f} mm")
            col2.metric("Média por Registro", f"{df_filtrado['precipitacao_mm'].mean():.1f} mm")
            col3.metric("Maior Chuva Registrada", f"{df_filtrado['precipitacao_mm'].max():.1f} mm")

            st.divider()

            # Gráficos
            col_left, col_right = st.columns(2)

            with col_left:
                st.subheader("Evolução Temporal por Cidade")
                fig_linha = px.line(
                    df_filtrado, 
                    x="data", 
                    y="precipitacao_mm", 
                    color="cidade",
                    labels={"precipitacao_mm": "Chuva (mm)", "data": "Data"},
                    template="plotly_white"
                )
                st.plotly_chart(fig_linha, use_container_width=True)

            with col_right:
                st.subheader("Mapa da Precipitação")
                fig_mapa = px.scatter_mapbox(
                    df_filtrado,
                    lat="latitude",
                    lon="longitude",
                    size="precipitacao_mm",
                    color="precipitacao_mm",
                    hover_name="cidade",
                    hover_data=["data", "precipitacao_mm"],
                    color_continuous_scale="Blues",
                    size_max=35,
                    zoom=5.5,
                    mapbox_style="open-street-map"
                )
                st.plotly_chart(fig_mapa, use_container_width=True)

            st.subheader("Tabela de Dados")
            st.dataframe(df_filtrado.sort_values(by="data", ascending=False), use_container_width=True)
