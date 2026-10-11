// Dimensão de compradores (um registro por Comprador_ID)
let
    Colunas = Table.SelectColumns(Fato_Vendas_Ingressos, {"Comprador_ID", "Cidade_Comprador", "UF_Comprador", "Pais_Comprador"}),
    Unicos = Table.Distinct(Colunas, {"Comprador_ID"}),
    ComTipo = Table.AddColumn(Unicos, "Tipo_Comprador", each
        if [Pais_Comprador] = "Brasil" then "Nacional" else "Estrangeiro", type text),
    Ordenada = Table.Sort(ComTipo, {{"Comprador_ID", Order.Ascending}})
in
    Ordenada
