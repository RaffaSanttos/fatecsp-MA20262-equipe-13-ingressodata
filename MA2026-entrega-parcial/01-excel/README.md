# 01-excel · Etapa 1: Excel Avançado

**Arquivo principal:** `IngressoData_01_Excel.xlsx` (salvo e recalculado no Excel em 25/11/2026: Auditoria **APROVADO**, 0 erros de fórmula).
**Com macros:** `IngressoData_01_Excel.xlsm`, a mesma planilha com os módulos VBA e botões na aba Leia_me (ver `MA2026-entrega-final/01-vba`).

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

## Validação, formatação condicional e ÍNDICE/CORRESP

| Recurso | Onde | Regra |
|---|---|---|
| Validação de dados (personalizada) | `DePara_*` coluna A | Original em minúsculas, sem espaços sobrando e sem repetir (`E(EXATO(A2;MINÚSCULA(ARRUMAR(A2)));CONT.SE(...)=1)`) |
| Validação de dados (lista) | `DePara_Categoria` B, `Cadastro_Eventos` B | Show, Festival ou Cinema |
| Validação de dados (lista com aviso) | `DePara_Pais` B, `Cadastro_Eventos` C | País/praça fora da lista só entra depois de confirmar |
| Validação de dados (lista e data) | `Cadastro_Eventos` E e F | Sim/Não; data entre 01/01/2024 e 31/12/2030 |
| Formatação condicional | `Tratamento` | Status "Descartar…" e Duplicado "Sim" em vermelho; "REVISAR" em amarelo |
| Formatação condicional | `Auditoria` | Semáforo: verde quando OK/0/APROVADO, vermelho quando há problema |
| Formatação condicional | `Resumo_KPIs` | Barras de dados em % turista e participação; escala de cor no faturamento por praça; % turista ≥ 40% em verde |
| ÍNDICE + CORRESP duplo | `Resumo_KPIs`, linha 28 | Escolha um evento na lista (B30): a linha vem do `CORRESP` do evento e a coluna do `CORRESP` do nome do campo no cabeçalho do `Cadastro_Eventos`. Faturamento, ingressos e % turista do evento vêm de `SOMASES` |

## Dados brutos

Pasta `dados-brutos/`: `vendas_SP.xlsx`, `vendas_RJ.xlsx`, `vendas_MG.csv` e `tabelas_apoio.xlsx` (De-Para e cadastros). Os mesmos arquivos alimentam o Power Query.

> Ao abrir no Excel, todas as fórmulas são recalculadas. No Excel em português as funções aparecem traduzidas (XLOOKUP = PROCX, NUMBERVALUE = VALORNUMERO, TRIM = ARRUMAR).
