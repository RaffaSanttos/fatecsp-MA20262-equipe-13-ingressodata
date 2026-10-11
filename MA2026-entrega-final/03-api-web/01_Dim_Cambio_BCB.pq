// Cotação PTAX do dólar (Banco Central, API Olinda/OData, sem chave).
// Uma linha por dia do calendário: fins de semana e feriados repetem a última cotação útil.
let
    Inicio = Date.ToText(List.Min(Dim_Calendario[Data]), "MM-dd-yyyy"),
    Fim = Date.ToText(List.Min({List.Max(Dim_Calendario[Data]), Date.From(DateTime.LocalNow())}), "MM-dd-yyyy"),
    Url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
        & "CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
        & "?@dataInicial='" & Inicio & "'&@dataFinalCotacao='" & Fim & "'"
        & "&$format=json&$select=cotacaoCompra,cotacaoVenda,dataHoraCotacao",
    Resposta = Json.Document(Web.Contents(Url)),
    Cotacoes = Table.FromRecords(Resposta[value]),
    ComData = Table.AddColumn(Cotacoes, "Data", each Date.FromText(Text.Start([dataHoraCotacao], 10)), type date),
    UltimaDoDia = Table.Group(ComData, {"Data"}, {
        {"Dolar_Compra", each List.Last([cotacaoCompra]), type number},
        {"Dolar_Venda", each List.Last([cotacaoVenda]), type number}}),
    Calendario = Table.SelectColumns(Dim_Calendario, {"Data"}),
    Juntado = Table.NestedJoin(Calendario, {"Data"}, UltimaDoDia, {"Data"}, "Cotacao", JoinKind.LeftOuter),
    Expandido = Table.ExpandTableColumn(Juntado, "Cotacao", {"Dolar_Compra", "Dolar_Venda"}),
    Ordenado = Table.Sort(Expandido, {{"Data", Order.Ascending}}),
    Preenchido = Table.FillDown(Ordenado, {"Dolar_Compra", "Dolar_Venda"}),
    SemVazios = Table.SelectRows(Preenchido, each [Dolar_Venda] <> null),
    Tipos = Table.TransformColumnTypes(SemVazios, {{"Data", type date}, {"Dolar_Compra", type number}, {"Dolar_Venda", type number}})
in
    Tipos
