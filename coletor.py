"""
SISTER-Clima | Coletor de Dados Pluviométricos
================================================
Componente do ecossistema SISTER (Sistema Integrado de Suporte à
Transição e Resiliência) — Projeto Resiliência, Embrapa.

Fonte de dados: Open-Meteo API (https://open-meteo.com/)
  Endpoint utilizado: /v1/forecast (dados de saída de modelo NWP)
  Nota técnica: os valores de precipitação coletados representam
  estimativas de modelo numérico de tempo (NWP), NÃO observações
  diretas de estações pluviométricas. Para análise climatológica
  de séries longas, considere o endpoint ERA5 Archive.

Licença: GNU GPLv3
"""

import os
import requests
import pandas as pd
from datetime import datetime, timedelta

# Lista de municípios monitorados no Rio Grande do Sul
MUNICIPIOS_RS = [
    {"cidade": "Porto Alegre",    "lat": -30.0346, "lon": -51.2177},
    {"cidade": "Caxias do Sul",   "lat": -29.1681, "lon": -51.1794},
    {"cidade": "Pelotas",         "lat": -31.7654, "lon": -52.3376},
    {"cidade": "Santa Maria",     "lat": -29.6842, "lon": -53.8069},
    {"cidade": "Passo Fundo",     "lat": -28.2625, "lon": -52.4083},
    {"cidade": "Bagé",            "lat": -31.3314, "lon": -54.1069},
    {"cidade": "Uruguaiana",      "lat": -29.7547, "lon": -57.0883},
    {"cidade": "Santa Cruz do Sul","lat": -29.7186, "lon": -52.4311},
    {"cidade": "Rio Grande",      "lat": -32.0350, "lon": -52.0986},
    {"cidade": "Lajeado",         "lat": -29.4669, "lon": -51.9614}
]

CSV_PATH = "data/chuva_diaria.csv"

def executar_coleta():
    """
    Coleta a precipitação estimada pelo modelo NWP (Open-Meteo /v1/forecast)
    para o dia anterior e atualiza incrementalmente o arquivo CSV.
    """
    data_alvo = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    novos_registros = []

    print(f"[SISTER-Clima] Iniciando coleta para: {data_alvo}")
    print(f"[SISTER-Clima] Fonte: Open-Meteo API (saída de modelo NWP)")

    for item in MUNICIPIOS_RS:
        # Endpoint de previsão/análise recente (modelo numérico)
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": item["lat"],
            "longitude": item["lon"],
            "daily": "precipitation_sum",
            "timezone": "America/Sao_Paulo",
            "start_date": data_alvo,
            "end_date": data_alvo
        }

        try:
            res = requests.get(url, params=params, timeout=15)
            res.raise_for_status()
            data = res.json()

            precipitacao_mm = data["daily"]["precipitation_sum"][0]
            novos_registros.append({
                "data": data_alvo,
                "cidade": item["cidade"],
                "latitude": item["lat"],
                "longitude": item["lon"],
                "precipitacao_mm": precipitacao_mm if precipitacao_mm is not None else 0.0,
                "fonte": "Open-Meteo NWP"
            })
            print(f"  ✓ {item['cidade']}: {precipitacao_mm} mm")
        except Exception as err:
            print(f"  ✗ Erro em {item['cidade']}: {err}")

    if not novos_registros:
        print("[SISTER-Clima] Nenhum dado coletado.")
        return

    df_novos = pd.DataFrame(novos_registros)

    # Atualização incremental da base — evita duplicatas por data+cidade
    os.makedirs("data", exist_ok=True)
    if os.path.exists(CSV_PATH):
        df_existente = pd.read_csv(CSV_PATH)
        df_final = pd.concat([df_existente, df_novos]).drop_duplicates(
            subset=["data", "cidade"], keep="last"
        )
    else:
        df_final = df_novos

    df_final.sort_values(by=["data", "cidade"], inplace=True)
    df_final.to_csv(CSV_PATH, index=False)
    print(f"[SISTER-Clima] Base atualizada: '{CSV_PATH}' ({len(df_final)} registros)")

if __name__ == "__main__":
    executar_coleta()
