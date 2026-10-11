# 03-powerpivot · Etapa 2: Star Schema e DAX

| Arquivo | Conteúdo |
|---|---|
| `IngressoData_03_PowerPivot.xlsx` | Aba `Modelo_e_DAX` (relacionamentos, medidas e valores esperados) + Fato e 4 dimensões como Tabelas do Excel |
| `medidas.dax` | As 14 medidas prontas para colar no Power Pivot ou no Power BI |
| `gabarito.json` | Números esperados para conferir o modelo |

## Montagem (Excel para Windows; o Excel para Mac não tem Power Pivot)

1. Caminho principal: carregar as consultas do `02-powerquery` no Modelo de Dados. Alternativa: nesta planilha, clique em cada tabela e use **Power Pivot > Adicionar ao Modelo de Dados**.
2. **Power Pivot > Gerenciar > Exibição de Diagrama**: crie os 4 relacionamentos da aba `Modelo_e_DAX` (todas as dimensões ligadas à fato, muitos para um).
3. Em `Dim_Calendario`: **Design > Marcar como Tabela de Data** (coluna `Data`).
4. Na área de cálculo da `Fato_Vendas_Ingressos`, cole cada medida de `medidas.dax` no formato `Nome := fórmula`.
5. Confira com uma Tabela Dinâmica do modelo: Faturamento Total = R$ 2.037.612,50; Ticket Médio = R$ 535,65; % Faturamento Turista = 42,74%.

## Star Schema

- **Fato_Vendas_Ingressos** (2.000 linhas): uma linha por venda.
- **Dim_Evento** (11), **Dim_Praca** (3), **Dim_Comprador** (932), **Dim_Calendario** (730).
