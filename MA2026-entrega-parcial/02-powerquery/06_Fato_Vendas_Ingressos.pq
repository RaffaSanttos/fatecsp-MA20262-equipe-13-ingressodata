// Tabela fato: consolida SP + RJ + MG, limpa, padroniza e classifica o público
let
    Empilhado = Table.Combine({Vendas_SP, Vendas_RJ, Vendas_MG}),
    SemVazias = Table.SelectRows(Empilhado, each [ID_Venda] <> null and Text.Trim(Text.From([ID_Venda])) <> ""),
    SemDuplicadas = Table.Distinct(SemVazias, {"ID_Venda"}),

    MapaCategoria = Record.FromList(DePara_Categoria[Padrao], DePara_Categoria[Original]),
    MapaCidade = Record.FromList(DePara_Cidade[Padrao], DePara_Cidade[Original]),
    MapaPais = Record.FromList(DePara_Pais[Padrao], DePara_Pais[Original]),
    Padronizar = (mapa as record, valor as any) as text =>
        Record.FieldOrDefault(mapa, Text.Lower(Text.Trim(Text.From(valor))), "REVISAR"),

    Tratada = Table.TransformColumns(SemDuplicadas, {
        {"ID_Venda", each Text.Trim(Text.From(_)), type text},
        {"Data_Venda", fnTratarData, type date},
        {"Data_Evento", fnTratarData, type date},
        {"Evento", each Text.Trim(Text.From(_)), type text},
        {"Categoria", each Padronizar(MapaCategoria, _), type text},
        {"Cidade_Evento", each Padronizar(MapaCidade, _), type text},
        {"Tipo_Ingresso", each Text.Trim(Text.From(_)), type text},
        {"Qtd", fnTratarNumero, Int64.Type},
        {"Valor_Unitario", fnTratarNumero, Currency.Type},
        {"Canal", each Text.Trim(Text.From(_)), type text},
        {"Comprador_ID", each Text.Trim(Text.From(_)), type text},
        {"Cidade_Comprador", each Padronizar(MapaCidade, _), type text},
        {"UF_Comprador", each Text.Upper(Text.Trim(Text.From(_))), type text},
        {"Pais_Comprador", each Padronizar(MapaPais, _), type text}
    }),
    Validas = Table.SelectRows(Tratada, each [Qtd] > 0 and [Valor_Unitario] > 0),
    ComTotal = Table.AddColumn(Validas, "Valor_Total", each [Qtd] * [Valor_Unitario], Currency.Type),
    ComOrigemPublico = Table.AddColumn(ComTotal, "Origem_Publico", each
        if [Pais_Comprador] <> "Brasil" then "Turista Internacional"
        else if [Cidade_Comprador] = [Cidade_Evento] then "Local"
        else "Turista Nacional", type text),
    Final = Table.SelectColumns(ComOrigemPublico, {
        "ID_Venda", "Data_Venda", "Data_Evento", "Evento", "Categoria", "Cidade_Evento", "Tipo_Ingresso",
        "Qtd", "Valor_Unitario", "Valor_Total", "Canal", "Comprador_ID", "Cidade_Comprador",
        "UF_Comprador", "Pais_Comprador", "Origem_Publico", "Arquivo_Origem"})
in
    Final
