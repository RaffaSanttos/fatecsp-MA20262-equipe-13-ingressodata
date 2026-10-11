// Lê uma aba de um arquivo .xlsx da pasta de dados, já com a primeira linha como cabeçalho
(arquivo as text, aba as text) as table =>
let
    Fonte = Excel.Workbook(File.Contents(pPastaDados & arquivo), true, true),
    Dados = Fonte{[Item = aba, Kind = "Sheet"]}[Data]
in
    Dados
