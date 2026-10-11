// Converte "R$ 1.250,00", "450,00", número ou vazio em número (vazio vira 0 e é descartado depois)
(valor as any) as number =>
let
    Texto = if valor = null or Value.Is(valor, type number) then "" else Text.Trim(Text.Replace(Text.From(valor), "R$", "")),
    Resultado =
        if valor = null then 0
        else if Value.Is(valor, type number) then valor
        else if Texto = "" then 0
        else try Number.FromText(Texto, "pt-BR") otherwise 0
in
    Resultado
