// Vendas brutas de SP (sem tratamento; o tratamento fica em Fato_Vendas_Ingressos)
let
    Fonte = fnLerAba("vendas_SP.xlsx", "Vendas"),
    ComOrigem = Table.AddColumn(Fonte, "Arquivo_Origem", each "vendas_SP.xlsx", type text)
in
    ComOrigem
