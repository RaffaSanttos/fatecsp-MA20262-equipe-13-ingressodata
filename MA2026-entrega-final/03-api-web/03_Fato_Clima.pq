// Clima diário das 3 praças no período das vendas. Chave para o modelo: Cidade + Data
let
    Inicio = List.Min(Fato_Vendas_Ingressos[Data_Venda]),
    Fim = List.Max(Fato_Vendas_Ingressos[Data_Evento]),
    PorPraca = Table.AddColumn(Dim_Praca, "Clima", each fnClimaPraca([Cidade], [Latitude], [Longitude], Inicio, Fim)),
    Combinado = Table.Combine(PorPraca[Clima]),
    ComChave = Table.AddColumn(Combinado, "Chave_Cidade_Data", each [Cidade] & "|" & Date.ToText([Data], "yyyy-MM-dd"), type text),
    ComFaixa = Table.AddColumn(ComChave, "Condicao", each
        if [Chuva_mm] = null then "Sem dado"
        else if [Chuva_mm] >= 10 then "Chuva forte"
        else if [Chuva_mm] >= 1 then "Chuva fraca"
        else "Seco", type text)
in
    ComFaixa
