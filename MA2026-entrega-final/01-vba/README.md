# 01-vba · Etapa 3: Automação com macros

`mdlRelatorioVendas.bas` gera relatórios de vendas por evento e praça a partir da tabela `tbVendasTratadas` (planilha do 01-excel).

| Macro | O que faz |
|---|---|
| RelatorioDiario | Vendas do último dia com movimento |
| RelatorioSemanal | Últimos 7 dias |
| RelatorioPeriodo | Pede data inicial e final |
| AtualizarDados | Atualiza Power Query e modelo (Atualizar Tudo) |

Cada relatório cria a aba `Rel_<tipo>_<aaaammdd>` com pedidos, ingressos, faturamento, faturamento turista, % turista e ticket médio, ordenada por faturamento.

`mdlAutomacaoPlanilha.bas` completa a etapa:

| Macro | O que faz |
|---|---|
| FormatarBaseTratada | Tarefa repetitiva: reaplica o padrão visual da aba Tratamento (fonte, cabeçalho, formatos de data e moeda, larguras, congelar painel). Escrita no formato do Gravador de Macros: para a aula 10, gravem a mesma formatação ao vivo e comparem |
| PrepararPastaComMacros | Cria 5 botões na aba Leia_me ligados às macros e salva a pasta como `IngressoData_01_Excel.xlsm` |

## Instalação

**Jeito rápido:** em `IngressoData_01_Excel.xlsx`, Alt + F11 > Arquivo > Importar Arquivo: `mdlRelatorioVendas.bas` e `mdlAutomacaoPlanilha.bas`. Depois Alt + F8 > `PrepararPastaComMacros`. O `.xlsm` com botões fica salvo ao lado do `.xlsx`.

**Passo a passo manual:**

1. Abra `IngressoData_01_Excel.xlsx`, pressione **Alt + F11**, **Arquivo > Importar Arquivo** e escolha o `.bas`.
2. Salve como **Pasta de Trabalho Habilitada para Macro (.xlsm)**.
3. **Alt + F8** > `RelatorioSemanal` > Executar. Opcional: inserir botões na aba Leia_me ligados às macros.

Não usa referências externas (sem Scripting.Dictionary), então roda no Excel para Windows e para Mac. Arquivo salvo em ANSI com quebras CRLF para o editor VBA ler os acentos corretamente.
