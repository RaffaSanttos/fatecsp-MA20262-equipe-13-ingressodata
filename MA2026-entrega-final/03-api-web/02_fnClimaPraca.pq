// Clima diário histórico de uma praça (Open-Meteo Archive API, gratuita e sem chave)
(cidade as text, latitude as number, longitude as number, inicio as date, fim as date) as table =>
let
    Url = "https://archive-api.open-meteo.com/v1/archive"
        & "?latitude=" & Number.ToText(latitude, "0.0000", "en-US")
        & "&longitude=" & Number.ToText(longitude, "0.0000", "en-US")
        & "&start_date=" & Date.ToText(inicio, "yyyy-MM-dd")
        & "&end_date=" & Date.ToText(fim, "yyyy-MM-dd")
        & "&daily=temperature_2m_max,precipitation_sum&timezone=America%2FSao_Paulo",
    Diario = Json.Document(Web.Contents(Url))[daily],
    Tabela = Table.FromColumns(
        {Diario[time], Diario[temperature_2m_max], Diario[precipitation_sum]},
        {"Data", "Temp_Max_C", "Chuva_mm"}),
    ComCidade = Table.AddColumn(Tabela, "Cidade", each cidade, type text),
    Tipos = Table.TransformColumnTypes(ComCidade, {{"Data", type date}, {"Temp_Max_C", type number}, {"Chuva_mm", type number}}, "en-US")
in
    Tipos
