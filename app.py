import streamlit as st
import pandas as pd
import plotly.express as px
import os
import io
import requests
from datetime import datetime, timedelta, date
import numpy as np
import plotly.figure_factory as ff

st.set_page_config(page_title="SISTER-Clima | Resiliência Climática", layout="wide", page_icon="🌧️", initial_sidebar_state="expanded")

# Injeção de CSS Customizado
custom_css = """
<style>
/* Ocultar o header padrão do Streamlit */
header[data-testid="stHeader"] {
    display: none !important;
}

/* Barra de Navegação Superior Fixa (Topbar) */
.app-topbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 56px;
    display: flex;
    align-items: center;
    padding: 0 20px;
    background: linear-gradient(90deg, #071e38, #0c2844 60%, #071e38);
    border-bottom: 1px solid rgba(255,255,255,.08);
    z-index: 999999;
}
.mini-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}
.brand-container {
    display: flex;
    flex-direction: column;
    line-height: 1.1;
}
.brand-super {
    color: #2ea8e8;
    font-size: .58rem;
    font-weight: 900;
    letter-spacing: .12em;
    text-transform: uppercase;
}
.brand-main {
    color: #ffffff;
    font-size: 1.0rem;
    font-weight: 800;
}
.topbar-center {
    flex: 1;
    color: rgba(218,234,248,.58);
    font-size: .73rem;
    font-weight: 700;
    letter-spacing: .04em;
    text-align: center;
}
.topbar-right {
    display: flex;
    align-items: center;
    gap: 10px;
}
.topbar-btn {
    border: 1px solid rgba(255,255,255,.16);
    border-radius: 999px;
    color: rgba(218,234,248,.84) !important;
    font-size: .7rem;
    font-weight: 800;
    padding: 5px 15px;
    text-decoration: none;
    transition: 0.3s;
}
.topbar-btn:hover {
    background: rgba(255,255,255,.08);
    color: #ffffff !important;
}

/* Ajustes de Padding para compensar a Topbar */
.main .block-container {
    padding-top: 80px !important;
}
[data-testid="stSidebar"] {
    padding-top: 56px !important;
}

/* Sidebar Dark Blue Background */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c2844, #071e38) !important;
}
/* Sidebar: estrutura flex para empurrar o footer */
[data-testid="stSidebar"] > div:first-child {
    display: flex !important;
    flex-direction: column !important;
    height: 100vh !important;
    overflow: hidden !important;
}
[data-testid="stSidebarUserContent"] {
    flex: 1 !important;
    display: flex !important;
    flex-direction: column !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    padding-bottom: 10px !important;
}
.sidebar-footer-container {
    margin-top: auto !important;
    flex-shrink: 0 !important;
}

/* Textos da Sidebar para Branco/Azul Claro */
[data-testid="stSidebar"] .css-17lntkn, 
[data-testid="stSidebar"] p, 
[data-testid="stSidebar"] div, 
[data-testid="stSidebar"] span, 
[data-testid="stSidebar"] label {
    color: #daeaf8 !important;
}
/* Customização dos Radio Buttons na Sidebar */
div[role="radiogroup"] label {
    background-color: transparent !important;
    padding: 10px;
    border-radius: 8px;
    transition: 0.3s;
}
div[role="radiogroup"] label:hover {
    background-color: rgba(255,255,255,0.07) !important;
}

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

/* Títulos Principais no Conteúdo */
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
.sidebar-logo-text {
    font-size: 1.15rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 20px;
    line-height: 1.25;
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
    padding-bottom: 10px;
}
.sidebar-footer-container {
    font-size: 0.72rem;
    color: rgba(255,255,255,0.45);
    border-top: 1px solid rgba(255,255,255,0.06);
    padding: 12px 10px 10px 10px;
    line-height: 1.5;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Renderizar a Barra Superior (Topbar) SISTER com Logo Oficial
st.markdown("""
<div class="app-topbar">
  <div class="mini-brand">
    <svg viewBox="0 0 64 64" aria-hidden="true" style="width:32px;height:32px;color:#2ea8e8;fill:none;stroke:currentColor;stroke-width:2.8;filter:drop-shadow(0 0 6px rgba(46,168,232,.38));">
      <g fill="none" stroke="currentColor" stroke-width="2.8"><path d="M32 5 55 18v28L32 59 9 46V18z"/><path d="M32 5v54M9 18l46 28M55 18 9 46"/></g>
      <g fill="currentColor"><circle cx="32" cy="5" r="4"/><circle cx="55" cy="18" r="4"/><circle cx="55" cy="46" r="4"/><circle cx="32" cy="59" r="4"/><circle cx="9" cy="46" r="4"/><circle cx="9" cy="18" r="4"/><circle cx="32" cy="32" r="5"/></g>
    </svg>
    <div class="brand-container">
      <span class="brand-super">SISTER</span>
      <span class="brand-main">Clima</span>
    </div>
  </div>
  <div class="topbar-center">SISTER-Clima | Painel de Resiliência Climática | Monitoramento Pluviométrico</div>
  <div class="topbar-right">
    <a href="https://github.com/jpereiratrindade/Sister-Clima" target="_blank" class="topbar-btn">Repositório GitHub</a>
  </div>
</div>
""", unsafe_allow_html=True)

# ---- Helper de Requisição Seguro ----
def fetch_url(url, proxy_settings, **kwargs):
    s = requests.Session()
    if proxy_settings.get("mode") == "Direta (Ignorar proxy do sistema)":
        s.trust_env = False  # Ignora totalmente variáveis de ambiente (SOCKS, HTTP_PROXY, etc)
    elif proxy_settings.get("mode") == "Proxy Customizado" and proxy_settings.get("custom_url"):
        s.proxies = {"http": proxy_settings["custom_url"], "https": proxy_settings["custom_url"]}
    return s.get(url, **kwargs)

# ---- Carregar Dados do IBGE via GitHub ----
@st.cache_data(ttl=24*3600)
def load_estados(proxy_settings):
    url = "https://raw.githubusercontent.com/kelvins/Municipios-Brasileiros/main/csv/estados.csv"
    res = fetch_url(url, proxy_settings, timeout=15)
    res.raise_for_status()
    df = pd.read_csv(io.StringIO(res.text))
    return df

@st.cache_data(ttl=24*3600)
def load_municipios(proxy_settings):
    url = "https://raw.githubusercontent.com/kelvins/Municipios-Brasileiros/main/csv/municipios.csv"
    res = fetch_url(url, proxy_settings, timeout=15)
    res.raise_for_status()
    df = pd.read_csv(io.StringIO(res.text))
    return df
    
@st.cache_data(ttl=24*3600)
def fetch_intra_municipal_surface(codigo_ibge, data_inicio, data_fim, proxy_settings):
    # Fetch GeoJSON
    url_geo = f"https://servicodados.ibge.gov.br/api/v3/malhas/municipios/{codigo_ibge}?formato=application/vnd.geo+json"
    res_geo = fetch_url(url_geo, proxy_settings, timeout=15)
    res_geo.raise_for_status()
    geojson = res_geo.json()
    
    lats, lons = [], []
    def extract_coords(coords):
        for c in coords:
            if isinstance(c[0], (list, tuple)):
                extract_coords(c)
            else:
                lons.append(c[0])
                lats.append(c[1])
                
    features = geojson.get("features", [])
    if features:
        extract_coords(features[0]["geometry"]["coordinates"])
        
    def point_in_polygon(x, y, poly):
        n = len(poly)
        inside = False
        p1x, p1y = poly[0]
        for i in range(n + 1):
            p2x, p2y = poly[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xints:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def point_in_multipolygon(x, y, geometry):
        coords = geometry["coordinates"]
        if geometry["type"] == "Polygon":
            coords = [coords]
        for polygon in coords:
            exterior = polygon[0]
            if point_in_polygon(x, y, exterior):
                in_hole = False
                for hole in polygon[1:]:
                    if point_in_polygon(x, y, hole):
                        in_hole = True
                        break
                if not in_hole:
                    return True
        return False
        
    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    
    # Generate high-density grid (0.05 degree ~ 5.5km) to avoid gaps
    step = 0.05
    grid_lats = np.arange(min_lat, max_lat + step, step)
    grid_lons = np.arange(min_lon, max_lon + step, step)
    
    geometry = features[0]["geometry"]
    coords = []
    for lat in grid_lats:
        for lon in grid_lons:
            if point_in_multipolygon(lon, lat, geometry):
                coords.append((lat, lon))
    
    # Cap to avoid extreme API loads on giant regions (safety)
    if len(coords) > 400:
        step = 0.1
        grid_lats = np.arange(min_lat, max_lat + step, step)
        grid_lons = np.arange(min_lon, max_lon + step, step)
        coords = []
        for lat in grid_lats:
            for lon in grid_lons:
                if point_in_multipolygon(lon, lat, geometry):
                    coords.append((lat, lon))

    rows = []
    chunk_size = 50
    om_url = "https://archive-api.open-meteo.com/v1/archive"
    
    for i in range(0, len(coords), chunk_size):
        chunk = coords[i:i+chunk_size]
        lat_str = ",".join([str(round(c[0], 4)) for c in chunk])
        lon_str = ",".join([str(round(c[1], 4)) for c in chunk])
        params = {
            "latitude": lat_str,
            "longitude": lon_str,
            "start_date": data_inicio.strftime("%Y-%m-%d"),
            "end_date": data_fim.strftime("%Y-%m-%d"),
            "daily": "precipitation_sum",
            "timezone": "America/Sao_Paulo"
        }
        res = fetch_url(om_url, proxy_settings, params=params, timeout=25)
        res.raise_for_status()
        data_om = res.json()
        if isinstance(data_om, dict): 
            data_om = [data_om]
        for j, site_data in enumerate(data_om):
            if "daily" in site_data and "precipitation_sum" in site_data["daily"]:
                vals = site_data["daily"]["precipitation_sum"]
                total = sum([v for v in vals if v is not None])
                rows.append({"latitude": chunk[j][0], "longitude": chunk[j][1], "Total (mm)": total})
                
    return pd.DataFrame(rows), geojson, min_lat, max_lat, min_lon, max_lon

# ==========================================
# SIDEBAR (Navegação & Configuração)
# ==========================================
with st.sidebar:
    st.markdown('<div class="sidebar-logo-text">Resiliência Climática</div>', unsafe_allow_html=True)
    
    with st.expander("🌐 Configuração de Rede (Proxy)", expanded=False):
        proxy_mode = st.radio("Conexão:", ["Direta (Ignorar proxy do sistema)", "Usar Proxy do Sistema", "Proxy Customizado"])
        custom_proxy = ""
        if proxy_mode == "Proxy Customizado":
            custom_proxy = st.text_input("URL do Proxy (ex: http://proxy:8080 ou socks5://...)")
            if not custom_proxy.startswith("http") and not custom_proxy.startswith("socks") and custom_proxy:
                custom_proxy = "http://" + custom_proxy
        
        proxy_settings = {
            "mode": proxy_mode,
            "custom_url": custom_proxy
        }

    menu_selecionado = st.radio(
        "Navegação:",
        ["🌎 Explorador Nacional", "📊 Operação Consolidada", "📖 Sobre os Dados"],
        label_visibility="collapsed"
    )

try:
    df_estados = load_estados(proxy_settings)
    df_municipios = load_municipios(proxy_settings)
except Exception as e:
    st.error(f"Erro ao carregar dados. Verifique a configuração de rede/proxy na barra lateral. Detalhe: {e}")
    st.stop()

with st.sidebar:
    # Timestamp = data da última coleta real (última entrada do CSV)
    ultima_coleta = "Sem dados ainda"
    CSV_PATH_CHECK = "data/chuva_diaria.csv"
    if os.path.exists(CSV_PATH_CHECK):
        try:
            df_check = pd.read_csv(CSV_PATH_CHECK, usecols=["data"])
            ultima_data = pd.to_datetime(df_check["data"]).max()
            ultima_coleta = ultima_data.strftime("%d/%m/%Y")
        except Exception:
            ultima_coleta = "Erro ao ler"
            
    st.write("")
    if st.button("🔄 Sincronizar GitHub", use_container_width=True, help="Baixa os dados mais recentes gerados pelo robô (Git Pull)"):
        with st.spinner("Sincronizando..."):
            import subprocess
            try:
                subprocess.run(["git", "pull", "--rebase"], check=True, capture_output=True)
                st.success("Base local atualizada!")
                import time; time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error("Erro na sincronização.")
    st.markdown(
        f'<div class="sidebar-footer-container">'
        f'<b style="color:rgba(255,255,255,0.7);font-size:0.7rem;">SISTER-Clima v2.3</b><br>'
        f'© 2026 Embrapa<br>'
        f'Fontes: <a href="https://open-meteo.com" target="_blank" style="color:#5ec8f5;">Open-Meteo</a>'
        f' &amp; <a href="https://power.larc.nasa.gov" target="_blank" style="color:#5ec8f5;">NASA POWER</a><br>'
        f'<span style="font-size:0.65rem;opacity:0.6;">NWP · ERA5 · MERRA-2</span><br>'
        f'<span style="font-size:0.65rem;opacity:0.55;">Coleta RS: {ultima_coleta}</span>'
        f'</div>',
        unsafe_allow_html=True
    )

# ==========================================
# CONTEÚDO PRINCIPAL
# ==========================================
st.markdown('<div class="main-title">🌧️ SISTER-Clima | Monitoramento Climático</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Monitoramento pluviométrico com múltiplas fontes de dados &mdash; <a href="https://open-meteo.com" target="_blank" style="color:#2ea8e8;text-decoration:none;font-weight:700;">Open-Meteo</a> (NWP · ERA5) e <a href="https://power.larc.nasa.gov" target="_blank" style="color:#2ea8e8;text-decoration:none;font-weight:700;">NASA POWER</a> (MERRA-2)</div>', unsafe_allow_html=True)
st.divider()

if menu_selecionado == "🌎 Explorador Nacional":
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
        fonte_dados = st.radio(
            "Fonte de Dados:",
            ["🟡 Open-Meteo (NWP)", "🚀 NASA POWER (MERRA-2)"],
            help="Open-Meteo: livre para pesquisa. NASA POWER: domínio público, irrestrito para qualquer uso."
        )

    buscar = st.button("Gerar Relatório (Últimos 30 dias)", type="primary", use_container_width=True)

    # Card descritivo da fonte selecionada
    if "NASA POWER" in fonte_dados:
        with st.expander("🚀 NASA POWER MERRA-2 — Uso irrestrito", expanded=True):
            col_desc1, col_desc2 = st.columns([2, 1])
            with col_desc1:
                st.markdown(
                    "**O que é o NASA POWER?**\n\n"
                    "A [NASA POWER API](https://power.larc.nasa.gov/) (Prediction Of Worldwide Energy Resources) "
                    "fornece dados meteorológicos derivados do modelo **MERRA-2** (Modern-Era Retrospective Analysis for Research and Applications). "
                    "É um produto de reanálise da NASA que assimila observações de satélites e estações para reconstruir o estado da atmosfera.\n\n"
                    "**Vantagens:**\n"
                    "- 🟢 **Licença irrestrita** — domínio público NASA, uso comercial e institucional liberado\n"
                    "- 🔑 **Sem chave de API** — acesso direto, sem cadastro\n"
                    "- 🌾 **Parâmetros agronômicos** — evapotranspiração, umidade, temperatura do solo\n"
                    "- 📅 **Histórico desde 1981** com resolução diária global\n"
                    "- 📍 Resolução espacial: ~0.5° × 0.625° (~50–70 km)"
                )
            with col_desc2:
                st.markdown("**Parâmetro utilizado:**")
                st.code("PRECTOTCORR\n(Precipitação Corrigida\nmm/dia)", language="text")
                st.markdown("⚠️ **Nota técnica:** MERRA-2 é reanálise, não observação direta de estação.", unsafe_allow_html=False)
    else:
        with st.expander("🟡 Open-Meteo NWP — Pesquisa e desenvolvimento", expanded=False):
            st.markdown(
                "**O que é o Open-Meteo NWP?**\n\n"
                "A [Open-Meteo API](https://open-meteo.com/) fornece saída de **modelos numéricos de tempo** (NWP) como ICON (DWD), "
                "GFS (NOAA) e ECMWF, além de dados históricos via ERA5 Reanalysis.\n\n"
                "⚠️ **Licença:** gratuito para uso **pessoal e não-comercial**. Uso institucional/comercial requer "
                "[plano pago](https://open-meteo.com/en/pricing).\n\n"
                "O parâmetro `precipitation_sum` representa a precipitação acumulada diária estimada pelo modelo, "
                "não uma observação direta de pluviometria."
            )

    if buscar:
        cidade_info = lista_municipios[lista_municipios["nome"] == municipio_sel_nome].iloc[0]
        lat, lon = cidade_info["latitude"], cidade_info["longitude"]

        end_dt = datetime.now()
        start_dt = end_dt - timedelta(days=30)

        try:
            if "NASA POWER" in fonte_dados:
                # ---- NASA POWER API (MERRA-2, sem chave, irrestrito) ----
                nasa_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
                nasa_params = {
                    "parameters": "PRECTOTCORR",
                    "community": "AG",
                    "longitude": lon,
                    "latitude": lat,
                    "start": start_dt.strftime("%Y%m%d"),
                    "end": end_dt.strftime("%Y%m%d"),
                    "format": "JSON"
                }
                res = fetch_url(nasa_url, proxy_settings, params=nasa_params, timeout=20)
                res.raise_for_status()
                data = res.json()
                raw = data["properties"]["parameter"]["PRECTOTCORR"]
                df_live = pd.DataFrame([
                    {"Data": pd.to_datetime(k, format="%Y%m%d"), "Chuva (mm)": max(v, 0.0)}
                    for k, v in raw.items()
                ]).sort_values("Data").reset_index(drop=True)
                fonte_label = "NASA POWER MERRA-2"
                fonte_badge = "🚀"
            else:
                # ---- Open-Meteo NWP ----
                url = "https://api.open-meteo.com/v1/forecast"
                params = {
                    "latitude": lat, "longitude": lon,
                    "daily": "precipitation_sum", "timezone": "America/Sao_Paulo",
                    "start_date": start_dt.strftime("%Y-%m-%d"),
                    "end_date": end_dt.strftime("%Y-%m-%d")
                }
                res = fetch_url(url, proxy_settings, params=params, timeout=15)
                res.raise_for_status()
                data = res.json()
                df_live = pd.DataFrame({
                    "Data": data["daily"]["time"],
                    "Chuva (mm)": data["daily"]["precipitation_sum"]
                })
                df_live["Data"] = pd.to_datetime(df_live["Data"])
                df_live["Chuva (mm)"] = df_live["Chuva (mm)"].fillna(0.0)
                fonte_label = "Open-Meteo NWP"
                fonte_badge = "🟡"

            df_live["Acumulado (mm)"] = df_live["Chuva (mm)"].cumsum()

            def categorizar_chuva(mm):
                if mm < 1: return "Sem Chuva"
                elif mm < 10: return "Leve (1-10mm)"
                elif mm < 25: return "Moderada (10-25mm)"
                else: return "Forte (>25mm)"

            df_live["Intensidade"] = df_live["Chuva (mm)"].apply(categorizar_chuva)


            st.divider()
            col_diag, col_fonte = st.columns([2, 1])
            with col_diag:
                st.markdown(f"#### Diagnóstico: **{municipio_sel_nome} - {estado_sel_nome}**")
            with col_fonte:
                st.markdown(f"<div style='text-align:right;padding-top:8px;font-size:0.8rem;color:#64748b;'>{fonte_badge} Fonte: <b>{fonte_label}</b></div>", unsafe_allow_html=True)
            
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
                    title="Distribuição Diária",
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
                    color_discrete_sequence=["#f59e0b"],
                    markers=True
                )
                fig2.update_traces(fill='tozeroy', fillcolor="rgba(245, 158, 11, 0.1)")
                fig2.update_layout(margin=dict(l=20, r=20, t=40, b=20), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig2, use_container_width=True)

            # --- ROW 3: DONUT E MAPA DE SUPERFÍCIE ---
            col_donut, col_map_single = st.columns([1, 1.5])
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
                
            with col_map_single:
                try:
                    cod_ibge = cidade_info["codigo_ibge"]
                    with st.spinner(f"Mapeando variação intra-municipal em alta resolução para {municipio_sel_nome}..."):
                        df_grid, geojson, min_lat, max_lat, min_lon, max_lon = fetch_intra_municipal_surface(
                            cod_ibge, start_dt, end_dt, proxy_settings
                        )
                        
                        # Densificação Espacial (Gap Filling):
                        # Cria uma nuvem de pontos ao redor de cada coordenada real para forçar o Plotly
                        # a preencher 100% da área de superfície sem deixar buracos entre os hexágonos.
                        oversampled = []
                        for _, row in df_grid.iterrows():
                            lat = row['latitude']
                            lon = row['longitude']
                            val = row['Total (mm)']
                            # 9 pontos preenchendo a área do pixel original
                            for dlat in [-0.02, 0, 0.02]:
                                for dlon in [-0.02, 0, 0.02]:
                                    oversampled.append({'latitude': lat + dlat, 'longitude': lon + dlon, 'Total (mm)': val})
                        df_grid_dense = pd.DataFrame(oversampled)
                        
                        if start_dt == end_dt:
                            periodo_str = f"Data: {start_dt.strftime('%d/%m/%Y')}"
                        else:
                            periodo_str = f"Período: {start_dt.strftime('%d/%m/%Y')} a {end_dt.strftime('%d/%m/%Y')}"
                        map_title = f"Superfície Intra-Municipal: {municipio_sel_nome}<br><sup>{periodo_str} (Acumulado)</sup>"
                        
                        try:
                            fig_map_single = ff.create_hexbin_map(
                                data_frame=df_grid_dense, lat="latitude", lon="longitude",
                                nx_hexagon=25, opacity=0.85, labels={"color": "Precipitação (mm)"},
                                color="Total (mm)", agg_func=np.mean,
                                min_count=1, color_continuous_scale="Blues",
                                title=map_title,
                                zoom=9
                            )
                        except AttributeError:
                            fig_map_single = ff.create_hexbin_mapbox(
                                data_frame=df_grid_dense, lat="latitude", lon="longitude",
                                nx_hexagon=25, opacity=0.85, labels={"color": "Precipitação (mm)"},
                                color="Total (mm)", agg_func=np.mean,
                                min_count=1, color_continuous_scale="Blues",
                                title=map_title,
                                zoom=9, mapbox_style="open-street-map"
                            )
                            
                        # Overlay IBGE GeoJSON
                        fig_map_single.update_layout(
                            mapbox={
                                "layers": [
                                    {
                                        "source": geojson,
                                        "type": "line",
                                        "color": "black",
                                        "line": {"width": 2}
                                    }
                                ],
                                "center": {"lat": (min_lat + max_lat) / 2, "lon": (min_lon + max_lon) / 2}
                            },
                            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=20, t=40, b=20)
                        )
                        st.plotly_chart(fig_map_single, use_container_width=True)
                except Exception as e:
                    st.error(f"Erro ao gerar mapa intra-municipal: {e}")

            # --- ROW 4: TABELA ---
            st.write("")
            st.markdown("**Registro Analítico Diário**")
            st.dataframe(
                df_live.sort_values(by="Data", ascending=False).style.format({"Chuva (mm)": "{:.1f}", "Acumulado (mm)": "{:.1f}"}),
                use_container_width=True, height=300
            )
        except Exception as e:
            st.error(f"Erro na comunicação com a API: {e}")

elif menu_selecionado == "📊 Operação Consolidada":
    st.markdown("### Controle Base Operacional - Rio Grande do Sul")
    st.markdown("Gestão dos dados salvos no repositório pela rotina de automação `daily_fetch`.")

    CSV_PATH = "data/chuva_diaria.csv"
    if not os.path.exists(CSV_PATH):
        st.warning("Nenhum arquivo 'chuva_diaria.csv' encontrado. Aguarde a automação ou execute o script de coleta.")
    else:
        df = pd.read_csv(CSV_PATH)
        df["data"] = pd.to_datetime(df["data"])

        # Obter siglas dos estados
        df_municipios["nome_uf"] = df_municipios["nome"] + " (" + df_municipios["codigo_uf"].map(df_estados.set_index("codigo_uf")["uf"]) + ")"

        # ---- LINHA 1: Cidades + Fonte de Dados ----
        col_sel1, col_sel2 = st.columns([1, 1])
        with col_sel1:
            cidades_sel = st.multiselect("Cidades Ativas (Histórico):", options=sorted(df["cidade"].unique()), default=df["cidade"].unique())
        with col_sel2:
            cidades_extras_sel = st.multiselect(
                "Adicionar Outros Municípios:",
                options=sorted(df_municipios["nome_uf"].unique()),
                help="Busca dados históricos adicionais em tempo real (Open-Meteo Archive) e plota junto com os dados locais do RS."
            )

        # ---- LINHA 2: Seletor de Período ----
        st.markdown("**Período de Análise:**")
        col_preset, col_datas = st.columns([1, 2])
        with col_preset:
            preset = st.selectbox(
                "Atalho:",
                ["Personalizado", "Últimos 7 dias", "Últimos 30 dias", "Últimos 90 dias", "Últimos 365 dias", "Todo o histórico"]
            )
        with col_datas:
            hoje = datetime.now().date()
            if preset == "Últimos 7 dias":
                data_inicio_def = hoje - timedelta(days=7)
                data_fim_def = hoje
            elif preset == "Últimos 30 dias":
                data_inicio_def = hoje - timedelta(days=30)
                data_fim_def = hoje
            elif preset == "Últimos 90 dias":
                data_inicio_def = hoje - timedelta(days=90)
                data_fim_def = hoje
            elif preset == "Últimos 365 dias":
                data_inicio_def = hoje - timedelta(days=365)
                data_fim_def = hoje
            elif preset == "Todo o histórico":
                data_inicio_def = df["data"].dt.date.min()
                data_fim_def = df["data"].dt.date.max()
            else:
                data_inicio_def = df["data"].dt.date.min()
                data_fim_def = df["data"].dt.date.max()

            datas_selecionadas = st.date_input(
                "Intervalo:",
                value=(data_inicio_def, data_fim_def),
                min_value=date(2020, 1, 1),
                max_value=hoje
            )

        if isinstance(datas_selecionadas, tuple) and len(datas_selecionadas) == 2:
            data_inicio, data_fim = datas_selecionadas
        else:
            data_inicio = data_fim = datas_selecionadas[0] if isinstance(datas_selecionadas, tuple) else datas_selecionadas

        # Filtrar dados históricos locais
        mask = (df["cidade"].isin(cidades_sel)) & (df["data"].dt.date >= data_inicio) & (df["data"].dt.date <= data_fim)
        df_filtrado = df[mask].copy()

        # Buscar dados extras
        if cidades_extras_sel:
            extra_dfs = []
            with st.spinner("Buscando dados no Open-Meteo Archive..."):
                for item in cidades_extras_sel:
                    cidade_info = df_municipios[df_municipios["nome_uf"] == item].iloc[0]
                    cidade_nome = cidade_info["nome"]
                    lat, lon = cidade_info["latitude"], cidade_info["longitude"]
                    uf_label = item.split("(")[-1].replace(")", "").strip()
                    label = f"{cidade_nome} ({uf_label})"

                    try:
                        archive_url = "https://archive-api.open-meteo.com/v1/archive"
                        params = {
                            "latitude": lat, "longitude": lon,
                            "start_date": data_inicio.strftime("%Y-%m-%d"),
                            "end_date": data_fim.strftime("%Y-%m-%d"),
                            "daily": "precipitation_sum", "timezone": "America/Sao_Paulo"
                        }
                        res = fetch_url(archive_url, proxy_settings, params=params, timeout=12)
                        res.raise_for_status()
                        data_api = res.json()
                        df_extra = pd.DataFrame({
                            "cidade": [label] * len(data_api["daily"]["time"]),
                            "data": pd.to_datetime(data_api["daily"]["time"]),
                            "precipitacao_mm": data_api["daily"]["precipitation_sum"],
                            "latitude": [lat] * len(data_api["daily"]["time"]),
                            "longitude": [lon] * len(data_api["daily"]["time"])
                        })
                        df_extra["precipitacao_mm"] = df_extra["precipitacao_mm"].fillna(0.0)

                        extra_dfs.append(df_extra)
                    except Exception as e:
                        st.warning(f"Não foi possível obter dados para {cidade_nome}: {e}")

            if extra_dfs:
                df_filtrado = pd.concat([df_filtrado, pd.concat(extra_dfs, ignore_index=True)], ignore_index=True)

        if df_filtrado.empty:
            st.info("Nenhum dado no período selecionado. Ajuste o intervalo ou adicione municípios extras.")
        else:
            st.divider()
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            kpi1.metric("Soma Total no Período", f"{df_filtrado['precipitacao_mm'].sum():.1f} mm")
            kpi2.metric("Média de Precipitação", f"{df_filtrado['precipitacao_mm'].mean():.1f} mm")
            kpi3.metric("Maior Evento Crítico", f"{df_filtrado['precipitacao_mm'].max():.1f} mm")
            kpi4.metric("Cidades Monitoradas", f"{df_filtrado['cidade'].nunique()}")

            st.write("")
            st.write("")
            col_chart, col_map = st.columns(2)
            with col_chart:
                fig_linha = px.line(
                    df_filtrado, x="data", y="precipitacao_mm", color="cidade",
                    title="Evolução Temporal Comparativa", template="plotly_white",
                    markers=True
                )
                fig_linha.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig_linha, use_container_width=True)

            with col_map:
                df_mapa = df_filtrado.groupby(["cidade", "latitude", "longitude"]).agg({"precipitacao_mm": "sum"}).reset_index()
                try:
                    fig_mapa = px.scatter_map(
                        df_mapa, lat="latitude", lon="longitude", size="precipitacao_mm", color="precipitacao_mm",
                        hover_name="cidade", color_continuous_scale="Blues",
                        size_max=35, zoom=5.5, title="Acumulado por Ponto (Bolhas)"
                    )
                except AttributeError:
                    fig_mapa = px.scatter_mapbox(
                        df_mapa, lat="latitude", lon="longitude", size="precipitacao_mm", color="precipitacao_mm",
                        hover_name="cidade", color_continuous_scale="Blues",
                        size_max=35, zoom=5.5, title="Acumulado por Ponto (Bolhas)", mapbox_style="open-street-map"
                    )
                fig_mapa.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig_mapa, use_container_width=True)


elif menu_selecionado == "📖 Sobre os Dados":
    st.markdown("### 📖 Transparência e Conformidade de Dados")
    st.markdown("Documentação técnica sobre as fontes de dados, limitações e roadmap de evolução do SISTER-Clima.")

    # ---- BLOCO 1: ALERTA DE CONFORMIDADE ----
    st.divider()
    st.markdown("#### ⚖️ Situação Atual — Open-Meteo API")
    col_a, col_b = st.columns([1.2, 1])
    with col_a:
        st.error(
            "**Restrição de Uso Comercial**\n\n"
            "A [Open-Meteo API](https://open-meteo.com/) é gratuita **apenas para uso pessoal e não-comercial**. "
            "Uso institucional, sistemas em produção ou aplicações comerciais requerem licença paga "
            "([open-meteo.com/en/pricing](https://open-meteo.com/en/pricing)).\n\n"
            "O SISTER-Clima v2.x utiliza Open-Meteo e, portanto, está autorizado apenas para **consumo particular e desenvolvimento**. "
            "Para implantação institucional plena (Embrapa), é necessária a migração para fontes abertas irrestrictas."
        )
    with col_b:
        st.info(
            "**O que isso significa?**\n\n"
            "✅ Uso pessoal e pesquisa: **liberado**\n\n"
            "✅ Desenvolvimento e testes: **liberado**\n\n"
            "⚠️ Sistema institucional interno: **verificar**\n\n"
            "❌ Produto comercial / SaaS: **requer licença**"
        )

    # ---- BLOCO 2: TIPOS DE DADO E RESOLUÇÃO ----
    st.divider()
    st.markdown("#### 🔬 NWP, Reanálise (MERRA-2/ERA5) ou Observação Real — Qual a diferença?")
    st.markdown(
        "Devido à natureza matemática dos modelos globais, **é esperado que haja forte discrepância entre os valores reportados por cada modelo** para o mesmo dia e local. Entenda o porquê:"
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
**🟡 Modelo NWP (Open-Meteo)**
*(Explorador Nacional)*

Modelos Numéricos de Tempo (ICON, GFS). Têm altíssima resolução, ideais para captar "células" isoladas de tempestade.

- **Foco:** Previsão e picos extremos.
- **Resolução Espacial:** ~7 a 11 km (pixel pequeno).
- **Comportamento:** Consegue isolar temporais locais, mas tende a **superestimar** picos em dados passados.
- **✅ Uso:** Defesa civil, risco pontual de alagamentos.
        """)
    with col2:
        st.markdown("""
**🚀 Reanálise (NASA POWER / ERA5)**
*(Operação Consolidada)*

Olha para o passado assimilando satélites e estações reais. Tira grandes médias espaciais, "achatando" picos isolados.

- **Foco:** Climatologia e agricultura.
- **Resolução Espacial:** ~50 km (pixel enorme).
- **Comportamento:** Excelente para volume total acumulado em bacias, mas dilui pancadas fortes isoladas.
- **✅ Uso:** Agroclimatologia, balanço hídrico de bacias, análise sazonal.
        """)
    with col3:
        st.markdown("""
**🟢 Observação Real (INMET/ANA)**
*(Planejado — v3.x)*

Leitura física direta de pluviômetros no terreno. É o dado exato que caiu naquele milímetro quadrado, sem estimativas.

- **Foco:** Hidrologia precisa e perícia.
- **Resolução:** Pontual (Local exato da estação).
- **Comportamento:** O único dado "real". Depende de a chuva ter caído exatamente sobre a estação.
- **✅ Uso:** Calibração de modelos, laudos, projetos de engenharia hídrica.
        """)

    # ---- BLOCO 3: COMPARAÇÃO ----
    st.divider()
    st.markdown("#### 🗂️ Comparativo de Fontes de Dados")
    df_fontes = pd.DataFrame({
        "Fonte": ["Open-Meteo (NWP)", "Open-Meteo (ERA5)", "NASA POWER ⭐", "INMET BDMEP ⭐", "ANA Hidroweb ⭐"],
        "Tipo": ["Modelo NWP", "Reanálise ERA5 ECMWF", "MERRA-2 NASA", "Observação real estação", "Pluviômetro hidrológico"],
        "Cobertura": ["Global", "Global (1940-)", "Global (1981-)", "Brasil (estações INMET)", "Brasil (bacias)"],
        "Chave API": ["❌ Nenhuma", "❌ Nenhuma", "❌ Nenhuma", "🔑 Token gratuito", "❌ Nenhuma"],
        "Uso Comercial": ["❌ Pago", "❌ Pago", "✅ Irrestrito (NASA)", "✅ Público BR", "✅ Público BR"],
        "Status": ["🟡 Em uso", "🟡 Em uso", "🔄 v3.0", "🔄 v3.0", "🔄 v3.1"]
    })
    st.dataframe(df_fontes, use_container_width=True, hide_index=True)
    st.caption("⭐ Fontes recomendadas para implantação institucional plena")

    # ---- BLOCO 4: ROADMAP ----
    st.divider()
    st.markdown("#### 🗺️ Roadmap — SISTER-Clima")
    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        st.markdown("""
**🟡 v2.x — Atual**

Open-Meteo API (NWP + ERA5)
- ✅ Funcional para P&D
- ⚠️ Licença restrita
- 5.570 municípios via IBGE
        """)
    with col_r2:
        st.markdown("""
**🔵 v3.0 — Planejada**

*NASA POWER API*
- Sem chave, sem custo
- Irrestrito (domínio público)
- Parâmetros agronômicos
- Ideal para missão Embrapa
        """)
    with col_r3:
        st.markdown("""
**🟢 v3.1 — Evolução**

*INMET + ANA Hidroweb*
- Observações reais de estações BR
- Token gratuito INMET
- Rede Hidroweb para bacias
- Conformidade MAPA/ANA
        """)

    # ---- BLOCO 5: NASA POWER ----
    st.divider()
    st.markdown("#### 🚀 Por que NASA POWER para a próxima versão?")
    col_nasa1, col_nasa2 = st.columns([1.5, 1])
    with col_nasa1:
        st.markdown(
            "A [NASA POWER API](https://power.larc.nasa.gov/) foi desenvolvida pelo NASA Langley Research Center "
            "para aplicações agrícolas e de energia renovável — **exatamente o domínio do Projeto Resiliência**.\n\n"
            "- 🌐 **Totalmente gratuita e irrestrita** — domínio público da NASA\n"
            "- 🌾 **Parâmetros agronômicos nativos**: evapotranspiração, umidade, temperatura\n"
            "- 📅 **Histórico desde 1981** via MERRA-2\n"
            "- 🗺️ Cobertura global (~50 km de resolução)\n"
            "- 📖 Citação: *NASA LaRC POWER Project, NASA Earth Science/Applied Science Program*"
        )
    with col_nasa2:
        st.code(
            "# Endpoint — sem autenticação\n"
            "GET power.larc.nasa.gov/api/\n"
            "  temporal/daily/point\n"
            "  ?parameters=PRECTOTCORR\n"
            "  &community=AG\n"
            "  &longitude=-51.2177\n"
            "  &latitude=-30.0346\n"
            "  &start=20240101\n"
            "  &end=20240131\n"
            "  &format=JSON",
            language="text"
        )
