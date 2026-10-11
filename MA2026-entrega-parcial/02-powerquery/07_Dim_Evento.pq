// Dimensão de eventos (cadastro em tabelas_apoio.xlsx). Data_Evento vazia = cinema com sessões diárias
let
    Fonte = fnLerAba("tabelas_apoio.xlsx", "Cadastro_Eventos"),
    Tipos = Table.TransformColumnTypes(Fonte, {
        {"Evento", type text}, {"Categoria", type text}, {"Cidade_Evento", type text},
        {"Local", type text}, {"Ao_Ar_Livre", type text}, {"Data_Evento", type date}})
in
    Tipos
