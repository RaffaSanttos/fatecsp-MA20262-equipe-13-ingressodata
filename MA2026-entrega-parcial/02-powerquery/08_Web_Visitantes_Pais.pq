// Web scraping: tabela "Visitantes que chegaram ao Brasil, por país de residência" da página
// Turismo no Brasil (Wikipédia, dados do Ministério do Turismo). A tabela vem no formato LARGO:
// uma linha por país e uma coluna por ano (2011 a 2025). O unpivot fica em Fato_Visitantes_Internacionais.
let
    Url = "https://pt.wikipedia.org/wiki/Turismo_no_Brasil",
    Pagina = Web.Page(Web.Contents(Url)),
    Candidatas = Table.SelectRows(Pagina, each
        [Caption] <> null and Text.Contains(Text.From([Caption]), "por país de residência")),
    Dados =
        if Table.IsEmpty(Candidatas)
        then error "Tabela de visitantes por país não encontrada. Confira se a página da Wikipédia mudou."
        else Candidatas{0}[Data],
    ComCabecalho =
        if Table.HasColumns(Dados, "País") then Dados
        else Table.PromoteHeaders(Dados, [PromoteAllScalars = true])
in
    ComCabecalho
