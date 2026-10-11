// Vendas brutas de RJ (sem tratamento; o tratamento fica em Fato_Vendas_Ingressos)
let
    Fonte = fnLerAba("vendas_RJ.xlsx", "Vendas"),
    ComOrigem = Table.AddColumn(Fonte, "Arquivo_Origem", each "vendas_RJ.xlsx", type text)
in
    ComOrigem
