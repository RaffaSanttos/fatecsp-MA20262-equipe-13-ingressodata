# 03-api-web · Etapa 5: Enriquecimento com APIs REST

| API | Dado | Chave? | Uso no projeto |
|---|---|---|---|
| Banco Central (Olinda/PTAX) `CotacaoDolarPeriodo` | Dólar compra/venda diário (JSON/OData) | não | Relacionar câmbio com compradores estrangeiros e ticket médio |
| Open-Meteo Archive `/v1/archive` | Temperatura máxima e chuva diária por coordenada | não | Clima no dia de eventos ao ar livre |

**Troca em relação à proposta:** o histórico de clima do OpenWeatherMap é pago (exige assinatura). O Open-Meteo entrega o mesmo dado de graça, sem cadastro, e mantém a justificativa original.

## Power Query (recomendado)

Colar como Consulta Nula, nesta ordem e com estes nomes: `Dim_Cambio_BCB`, `fnClimaPraca`, `Fato_Clima`, `Fato_Vendas_Enriquecida`. Dependem das consultas da entrega parcial (`Dim_Calendario`, `Dim_Praca`, `Fato_Vendas_Ingressos`). Na primeira atualização o Excel pede o nível de privacidade das fontes: escolha **Público**.

Resultado: a fato ganha `Dolar_no_Dia_da_Venda`, `Temp_Max_no_Evento`, `Chuva_mm_no_Evento` e `Condicao_no_Evento` (Seco, Chuva fraca, Chuva forte).

## Script Python (alternativa e carga no SQL)

```
python api_enriquecimento.py 2025-01-01 2026-06-30
```

Gera `dim_cambio.csv` e `fato_clima.csv` só com a biblioteca padrão. Testes offline: `python -m unittest test_api_enriquecimento` (4 testes passando).

**Execução real (22/11/2026):** `python api_enriquecimento.py 2025-01-01 2026-11-15` gerou `dados/dim_cambio.csv` (683 dias) e `dados/fato_clima.csv` (2.052 linhas = 3 praças × 684 dias). As mesmas consultas M rodaram no Power BI Desktop e alimentam o dashboard.

**Correção no Open-Meteo:** a API responde com `Content-Encoding: deflate` no formato zlib, que o Power Query não decodifica ("Dados inválidos encontrados durante a decodificação"). `fnClimaPraca` agora pede `Accept-Encoding: gzip`.
