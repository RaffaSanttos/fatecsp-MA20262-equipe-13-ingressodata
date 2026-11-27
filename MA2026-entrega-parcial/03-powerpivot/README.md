# 03-powerpivot · Etapa 2: Star Schema e DAX

| Arquivo | Conteúdo |
|---|---|
| **`IngressoData_03_PowerPivot.xlsm`** | **Entrega:** Modelo de Dados pronto (5 tabelas, 4 relacionamentos, 14 medidas DAX, `Dim_Calendario` marcada como Tabela de Data) + aba `Conferencia` com Tabela Dinâmica do modelo. Montado no Excel em 25/11/2026 |
| `IngressoData_03_PowerPivot.xlsx` | Ponto de partida sem modelo: aba `Modelo_e_DAX` (relacionamentos, medidas e valores esperados) + Fato e 4 dimensões como Tabelas do Excel |
| `mdlMontarModelo.bas` | Macro que monta o modelo a partir do `.xlsx` |
| `medidas.dax` | As 14 medidas prontas para colar no Power Pivot ou no Power BI |
| `gabarito.json` | Números esperados para conferir o modelo |

## Montagem com um clique (macro `mdlMontarModelo.bas`)

1. Abra `IngressoData_03_PowerPivot.xlsx` no Excel para Windows, Alt + F11 > Arquivo > Importar Arquivo > `mdlMontarModelo.bas`.
2. Alt + F8 > `MontarModeloPowerPivot`. A macro adiciona as 5 tabelas ao Modelo de Dados, cria os 4 relacionamentos e as 14 medidas DAX (com formato R$ e %), cria a aba `Conferencia` com uma Tabela Dinâmica do modelo e salva `IngressoData_03_PowerPivot.xlsm`.
3. Único passo manual: Power Pivot > Gerenciar > `Dim_Calendario` > Design > **Marcar como Tabela de Data** (o Excel não expõe esse comando ao VBA).
4. Confira na aba `Conferencia`: Faturamento Total R$ 2.037.612,50, Ticket Médio R$ 535,65, % Faturamento Turista 42,7%.

**Conferência do `.xlsm` (Tabela Dinâmica do modelo):** Cinema R$ 29.177,50 · Festival R$ 1.460.022,50 · Show R$ 548.412,50 · Total R$ 2.037.612,50, 3.804 ingressos, ticket R$ 535,65, 42,7% turista. `Faturamento Mês Anterior` de mar/2025 = faturamento de fev/2025 (R$ 22.932,50), confirmando o DATEADD.

Observação: no Excel em português o DAX usa `;` como separador de argumentos. A macro converte as vírgulas de `medidas.dax` automaticamente; ao colar à mão na área de cálculo, troque `,` por `;`.

O mesmo modelo (tabelas, relacionamentos e medidas) também está montado e conferido no Power BI: `MA2026-entrega-final/04-powerbi-dashboard/IngressoData_Dashboard.pbix`.

## Montagem manual (Excel para Windows; o Excel para Mac não tem Power Pivot)

1. Caminho principal: carregar as consultas do `02-powerquery` no Modelo de Dados. Alternativa: nesta planilha, clique em cada tabela e use **Power Pivot > Adicionar ao Modelo de Dados**.
2. **Power Pivot > Gerenciar > Exibição de Diagrama**: crie os 4 relacionamentos da aba `Modelo_e_DAX` (todas as dimensões ligadas à fato, muitos para um).
3. Em `Dim_Calendario`: **Design > Marcar como Tabela de Data** (coluna `Data`).
4. Na área de cálculo da `Fato_Vendas_Ingressos`, cole cada medida de `medidas.dax` no formato `Nome := fórmula`.
5. Confira com uma Tabela Dinâmica do modelo: Faturamento Total = R$ 2.037.612,50; Ticket Médio = R$ 535,65; % Faturamento Turista = 42,74%.

## Star Schema

- **Fato_Vendas_Ingressos** (2.000 linhas): uma linha por venda.
- **Dim_Evento** (11), **Dim_Praca** (3), **Dim_Comprador** (932), **Dim_Calendario** (730).
