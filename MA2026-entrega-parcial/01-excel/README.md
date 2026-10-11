# 01-excel · Etapa 1: Excel Avançado

**Arquivo principal:** `IngressoData_01_Excel.xlsx`

| Aba | O que faz |
|---|---|
| Leia_me | Fluxo da planilha e regras usadas |
| Base_Bruta | As 3 planilhas de vendas (SP, RJ, MG) empilhadas sem tratamento: 2.091 linhas |
| Tratamento | Tabela `tbVendasTratadas`: cada coluna é uma fórmula de limpeza |
| Auditoria | Conferência de linhas e de erros. Status atual: **APROVADO** (0 erros, 0 linhas sem De-Para) |
| Resumo_KPIs | Faturamento, ticket médio e % turista por categoria e por praça (SOMASES) + gráficos |
| DePara_* / Cadastro_Eventos | Tabelas de padronização usadas pelo PROCX (células amarelas = editáveis) |

## Problemas tratados e funções usadas

| Problema na base bruta | Solução |
|---|---|
| Datas em 3 formatos (texto dd/mm/aaaa, data do Excel, texto aaaa-mm-dd) | `SE`, `ÉNÚM`, `EXT.TEXTO`, `DATA`, `VALOR` |
| Valores em texto "R$ 1.250,00" e "450,00" | `VALORNUMERO(ARRUMAR(SUBSTITUIR(...)))` |
| Categorias e cidades escritas de vários jeitos (SHOW, Fest., BH, Sao Paulo...) | `PROCX(MINÚSCULA(ARRUMAR(...)); De-Para)` |
| 49 linhas duplicadas | `CONT.SE` acumulado no ID_Venda |
| 12 linhas vazias e 30 com quantidade/valor faltando | coluna `Status` descarta e a Auditoria explica cada descarte |
| Origem do comprador não classificada | `Origem_Publico`: Local, Turista Nacional ou Turista Internacional |

Resultado: **2.000 vendas válidas** (2.091 brutas = 12 vazias + 49 duplicadas + 30 inválidas + 2.000 OK).

## Dados brutos

Pasta `dados-brutos/`: `vendas_SP.xlsx`, `vendas_RJ.xlsx`, `vendas_MG.csv` e `tabelas_apoio.xlsx` (De-Para e cadastros). Os mesmos arquivos alimentam o Power Query.

> Ao abrir no Excel, todas as fórmulas são recalculadas. No Excel em português as funções aparecem traduzidas (XLOOKUP = PROCX, NUMBERVALUE = VALORNUMERO, TRIM = ARRUMAR).
