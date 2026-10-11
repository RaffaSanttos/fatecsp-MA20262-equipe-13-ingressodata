// Dimensão de praças (cidades-sede) com coordenadas usadas na API de clima
let
    Fonte = fnLerAba("tabelas_apoio.xlsx", "Cadastro_Pracas"),
    Tipos = Table.TransformColumnTypes(Fonte, {
        {"Cidade", type text}, {"UF", type text}, {"Regiao", type text},
        {"Latitude", type number}, {"Longitude", type number}})
in
    Tipos
