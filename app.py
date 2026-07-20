import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Chuva Diária RS", layout="wide", page_icon="🌧️")

st.title("🌧️ Monitoramento de Precipitação no RS")
st.markdown("Dados diários de chuva acumulada (mm) via Open-Meteo API.")

CSV_PATH = "data/chuva_diaria.csv"

if not os.path.exists(CSV_PATH):
    st.warning("Nenhum dado encontrado ainda. Execute o script `coletor.py` para gerar a base inicial.")
else:
    df = pd.read_csv(CSV_PATH)
    df["data"] = pd.to_datetime(df["data"])

    # Filtros na barra lateral
    st.sidebar.header("Filtros")
    cidades_sel = st.sidebar.multiselect(
        "Selecione as cidades:", 
        options=sorted(df["cidade"].unique()), 
        default=df["cidade"].unique()
    )

    datas_disponiveis = df["data"].dt.date.unique()
    data_inicio, data_fim = st.sidebar.date_input(
        "Período:",
        value=(min(datas_disponiveis), max(datas_disponiveis)),
        min_value=min(datas_disponiveis),
        max_value=max(datas_disponiveis)
    )

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
