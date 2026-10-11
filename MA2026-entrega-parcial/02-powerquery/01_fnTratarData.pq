// Converte qualquer formato de data das planilhas brutas em data:
// data/datahora do Excel (RJ), texto dd/mm/aaaa (SP) e texto aaaa-mm-dd (MG)
(valor as any) as nullable date =>
let
    Texto = if valor = null then "" else Text.Trim(Text.From(valor)),
    Resultado =
        if valor = null or Texto = "" then null
        else if Value.Is(valor, type date) then valor
        else if Value.Is(valor, type datetime) then Date.From(valor)
        else if Value.Is(valor, type number) then Date.From(valor)
        else if Text.Middle(Texto, 4, 1) = "-" then
            #date(
                Number.From(Text.Start(Texto, 4)),
                Number.From(Text.Middle(Texto, 5, 2)),
                Number.From(Text.Middle(Texto, 8, 2)))
        else
            #date(
                Number.From(Text.Middle(Texto, 6, 4)),
                Number.From(Text.Middle(Texto, 3, 2)),
                Number.From(Text.Start(Texto, 2)))
in
    Resultado
