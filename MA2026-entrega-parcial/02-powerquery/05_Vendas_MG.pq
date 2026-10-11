// Vendas brutas de MG: CSV separado por ";" em UTF-8
let
    Fonte = Csv.Document(
        File.Contents(pPastaDados & "vendas_MG.csv"),
        [Delimiter = ";", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cabecalhos = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    ComOrigem = Table.AddColumn(Cabecalhos, "Arquivo_Origem", each "vendas_MG.csv", type text)
in
    ComOrigem
