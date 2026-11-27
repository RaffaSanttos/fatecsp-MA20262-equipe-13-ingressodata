// Visitantes internacionais por país e ano: UNPIVOT da tabela larga raspada da web.
// Contexto externo para a pergunta central (quanto pesa o turista internacional nas vendas).
let
    Fonte = Web_Visitantes_Pais,
    // Remove o texto de notas de rodapé ("[30]") e deixa só os dígitos ("3 386 823" -> "3386823")
    SoDigitos = (valor as any) as text =>
        Text.Select(Text.Split(Text.From(valor), "["){0}, {"0".."9"}),
    SemNotas = Table.TransformColumns(Fonte, {{"País", each Text.Trim(Text.Split(Text.From(_), "["){0}), type text}}),
    SemTotais = Table.SelectRows(SemNotas, each not List.Contains({"Total", "Outros"}, [País])),

    // UNPIVOT: as colunas de ano viram linhas -> (País, Ano, Visitantes)
    Despivotado = Table.UnpivotOtherColumns(SemTotais, {"País"}, "Ano", "Visitantes"),

    ComAno = Table.TransformColumns(Despivotado, {
        {"Ano", each try Number.From(Text.Start(SoDigitos(_), 4)) otherwise null, Int64.Type},
        {"Visitantes", each try Number.From(SoDigitos(_)) otherwise null, Int64.Type}}),
    Validos = Table.SelectRows(ComAno, each [Ano] <> null and [Ano] >= 1990 and [Visitantes] <> null),

    // Mesmo De-Para de país da base de vendas (ex.: "Estados Unidos" -> "EUA"); sem De-Para mantém o nome
    MapaPais = Record.FromList(DePara_Pais[Padrao], DePara_Pais[Original]),
    PaisesVendas = List.Buffer(List.Distinct(Fato_Vendas_Ingressos[Pais_Comprador])),
    ComPais = Table.AddColumn(Validos, "Pais", each
        Record.FieldOrDefault(MapaPais, Text.Lower([País]), [País]), type text),
    ComFlag = Table.AddColumn(ComPais, "Pais_Na_Base_de_Vendas", each
        if List.Contains(PaisesVendas, [Pais]) then "Sim" else "Não", type text),
    Renomeado = Table.RenameColumns(ComFlag, {{"País", "Pais_Original"}}),
    Final = Table.Sort(
        Table.SelectColumns(Renomeado, {"Pais", "Pais_Original", "Ano", "Visitantes", "Pais_Na_Base_de_Vendas"}),
        {{"Ano", Order.Ascending}, {"Visitantes", Order.Descending}})
in
    Final
