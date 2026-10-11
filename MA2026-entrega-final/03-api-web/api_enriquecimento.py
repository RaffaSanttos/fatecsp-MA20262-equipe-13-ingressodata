"""Baixa câmbio (BCB/PTAX) e clima (Open-Meteo) e salva CSVs para o Power BI / banco SQL.

Uso:  python api_enriquecimento.py 2025-01-01 2026-06-30
Saída: dim_cambio.csv e fato_clima.csv na pasta atual. Só usa a biblioteca padrão do Python.
"""
import csv
import json
import sys
import urllib.parse
import urllib.request
from datetime import date, timedelta

URL_PTAX = ("https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
            "CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)")
URL_CLIMA = "https://archive-api.open-meteo.com/v1/archive"
PRACAS = {"São Paulo": (-23.5505, -46.6333), "Rio de Janeiro": (-22.9068, -43.1729),
          "Belo Horizonte": (-19.9167, -43.9345)}


def baixar_json(url):
    with urllib.request.urlopen(url, timeout=60) as resposta:
        return json.loads(resposta.read().decode("utf-8"))


def url_ptax(inicio, fim):
    parametros = (f"?@dataInicial='{inicio:%m-%d-%Y}'&@dataFinalCotacao='{fim:%m-%d-%Y}'"
                  "&$format=json&$select=cotacaoCompra,cotacaoVenda,dataHoraCotacao")
    return URL_PTAX + parametros


def ptax_por_dia(resposta, inicio, fim):
    """Última cotação de cada dia útil, repetida nos fins de semana e feriados."""
    cotacoes = {}
    for item in resposta["value"]:
        cotacoes[date.fromisoformat(item["dataHoraCotacao"][:10])] = (item["cotacaoCompra"], item["cotacaoVenda"])
    linhas, ultima, dia = [], None, inicio
    while dia <= fim:
        ultima = cotacoes.get(dia, ultima)
        if ultima:
            linhas.append({"Data": dia.isoformat(), "Dolar_Compra": ultima[0], "Dolar_Venda": ultima[1]})
        dia += timedelta(days=1)
    return linhas


def url_clima(latitude, longitude, inicio, fim):
    parametros = {"latitude": f"{latitude:.4f}", "longitude": f"{longitude:.4f}", "start_date": inicio.isoformat(),
                  "end_date": fim.isoformat(), "daily": "temperature_2m_max,precipitation_sum",
                  "timezone": "America/Sao_Paulo"}
    return URL_CLIMA + "?" + urllib.parse.urlencode(parametros)


def condicao(chuva_mm):
    if chuva_mm is None:
        return "Sem dado"
    if chuva_mm >= 10:
        return "Chuva forte"
    return "Chuva fraca" if chuva_mm >= 1 else "Seco"


def clima_da_praca(resposta, cidade):
    diario = resposta["daily"]
    return [{"Cidade": cidade, "Data": dia, "Temp_Max_C": temperatura, "Chuva_mm": chuva, "Condicao": condicao(chuva)}
            for dia, temperatura, chuva in zip(diario["time"], diario["temperature_2m_max"], diario["precipitation_sum"])]


def salvar_csv(caminho, linhas):
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(linhas[0]))
        escritor.writeheader()
        escritor.writerows(linhas)


def main(inicio, fim):
    cambio = ptax_por_dia(baixar_json(url_ptax(inicio, fim)), inicio, fim)
    salvar_csv("dim_cambio.csv", cambio)
    clima = []
    for cidade, (latitude, longitude) in PRACAS.items():
        clima += clima_da_praca(baixar_json(url_clima(latitude, longitude, inicio, fim)), cidade)
    salvar_csv("fato_clima.csv", clima)
    print(f"dim_cambio.csv: {len(cambio)} dias | fato_clima.csv: {len(clima)} linhas")


if __name__ == "__main__":
    main(date.fromisoformat(sys.argv[1]), date.fromisoformat(sys.argv[2]))
