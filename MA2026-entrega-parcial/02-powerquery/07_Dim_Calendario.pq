// Dimensão calendário: 1 linha por dia, do 1º dia do ano da primeira venda ao último dia do ano do último evento
let
    Inicio = #date(Date.Year(List.Min(Fato_Vendas_Ingressos[Data_Venda])), 1, 1),
    Fim = #date(Date.Year(List.Max(Fato_Vendas_Ingressos[Data_Evento])), 12, 31),
    Datas = List.Dates(Inicio, Duration.Days(Fim - Inicio) + 1, #duration(1, 0, 0, 0)),
    NomesMes = {"jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"},
    NomesDia = {"segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"},
    Tabela = Table.FromList(Datas, Splitter.SplitByNothing(), type table [Data = date]),
    Ano = Table.AddColumn(Tabela, "Ano", each Date.Year([Data]), Int64.Type),
    Mes = Table.AddColumn(Ano, "Mes", each Date.Month([Data]), Int64.Type),
    NomeMes = Table.AddColumn(Mes, "Nome_Mes", each NomesMes{[Mes] - 1}, type text),
    AnoMes = Table.AddColumn(NomeMes, "Ano_Mes", each Text.From([Ano]) & "-" & Text.PadStart(Text.From([Mes]), 2, "0"), type text),
    Trimestre = Table.AddColumn(AnoMes, "Trimestre", each "T" & Text.From(Date.QuarterOfYear([Data])), type text),
    DiaSemana = Table.AddColumn(Trimestre, "Dia_Semana", each NomesDia{Date.DayOfWeek([Data], Day.Monday)}, type text),
    FimDeSemana = Table.AddColumn(DiaSemana, "Fim_de_Semana", each if Date.DayOfWeek([Data], Day.Monday) >= 5 then "Sim" else "Não", type text)
in
    FimDeSemana
