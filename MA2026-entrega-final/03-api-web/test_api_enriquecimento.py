"""Testes offline com respostas no mesmo formato das APIs (rodar: python -m unittest)."""
import unittest
from datetime import date

import api_enriquecimento as api

RESPOSTA_PTAX = {"@odata.context": "...", "value": [
    {"cotacaoCompra": 5.1010, "cotacaoVenda": 5.1016, "dataHoraCotacao": "2025-01-03 13:05:22.123"},
    {"cotacaoCompra": 5.2000, "cotacaoVenda": 5.2006, "dataHoraCotacao": "2025-01-06 13:04:10.555"}]}
RESPOSTA_CLIMA = {"daily_units": {"time": "iso8601"}, "daily": {
    "time": ["2025-01-03", "2025-01-04", "2025-01-05"],
    "temperature_2m_max": [30.1, 27.4, None], "precipitation_sum": [0.0, 12.5, None]}}


class TesteCambio(unittest.TestCase):
    def test_fim_de_semana_repete_sexta(self):
        linhas = api.ptax_por_dia(RESPOSTA_PTAX, date(2025, 1, 2), date(2025, 1, 6))
        self.assertEqual([l["Data"] for l in linhas], ["2025-01-03", "2025-01-04", "2025-01-05", "2025-01-06"])
        self.assertEqual(linhas[1]["Dolar_Venda"], 5.1016)
        self.assertEqual(linhas[3]["Dolar_Venda"], 5.2006)

    def test_url_usa_formato_mm_dd_aaaa(self):
        url = api.url_ptax(date(2025, 1, 31), date(2025, 2, 1))
        self.assertIn("@dataInicial='01-31-2025'", url)
        self.assertIn("@dataFinalCotacao='02-01-2025'", url)


class TesteClima(unittest.TestCase):
    def test_condicao_e_nulos(self):
        linhas = api.clima_da_praca(RESPOSTA_CLIMA, "Rio de Janeiro")
        self.assertEqual([l["Condicao"] for l in linhas], ["Seco", "Chuva forte", "Sem dado"])
        self.assertEqual(linhas[0]["Cidade"], "Rio de Janeiro")

    def test_url_com_ponto_decimal(self):
        url = api.url_clima(-23.5505, -46.6333, date(2025, 1, 1), date(2025, 1, 31))
        self.assertIn("latitude=-23.5505", url)
        self.assertIn("daily=temperature_2m_max%2Cprecipitation_sum", url)


if __name__ == "__main__":
    unittest.main()
