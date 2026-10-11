// Tabela de padronização (Original em minúsculas -> Padrao). Editar em tabelas_apoio.xlsx
let
    Fonte = fnLerAba("tabelas_apoio.xlsx", "DePara_Cidade"),
    Tipos = Table.TransformColumnTypes(Fonte, {{"Original", type text}, {"Padrao", type text}})
in
    Tipos
