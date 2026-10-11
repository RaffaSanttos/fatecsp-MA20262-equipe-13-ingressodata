// Fato de vendas + câmbio do dia da venda + clima do dia do evento (enriquecimento via API)
let
    Fonte = Fato_Vendas_Ingressos,
    ComCambio = Table.NestedJoin(Fonte, {"Data_Venda"}, Dim_Cambio_BCB, {"Data"}, "Cambio", JoinKind.LeftOuter),
    CambioExpandido = Table.ExpandTableColumn(ComCambio, "Cambio", {"Dolar_Venda"}, {"Dolar_no_Dia_da_Venda"}),
    ComChave = Table.AddColumn(CambioExpandido, "Chave_Cidade_Data", each [Cidade_Evento] & "|" & Date.ToText([Data_Evento], "yyyy-MM-dd"), type text),
    ComClima = Table.NestedJoin(ComChave, {"Chave_Cidade_Data"}, Fato_Clima, {"Chave_Cidade_Data"}, "Clima", JoinKind.LeftOuter),
    ClimaExpandido = Table.ExpandTableColumn(ComClima, "Clima", {"Temp_Max_C", "Chuva_mm", "Condicao"},
        {"Temp_Max_no_Evento", "Chuva_mm_no_Evento", "Condicao_no_Evento"}),
    Tipos = Table.TransformColumnTypes(ClimaExpandido, {{"Dolar_no_Dia_da_Venda", type number}, {"Temp_Max_no_Evento", type number}, {"Chuva_mm_no_Evento", type number}})
in
    Tipos
