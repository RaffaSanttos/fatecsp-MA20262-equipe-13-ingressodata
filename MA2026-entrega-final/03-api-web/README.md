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

Endpoints conferidos na documentação pública do BCB e do Open-Meteo; a chamada real não foi executada daqui (rede bloqueada no ambiente de geração). Rode uma vez na máquina de vocês antes da apresentação.
