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
| FormatarBaseTratada | Tarefa repetitiva: reaplica o padrão visual da aba Tratamento (fonte, cabeçalho, formatos de data e moeda, larguras, congelar painel). Versão escrita e organizada à mão |
| PrepararPastaComMacros | Cria 5 botões na aba Leia_me ligados às macros e salva a pasta como `IngressoData_01_Excel.xlsm` |

`mdlMacroGravada.bas` tem a macro **gravada de verdade** com o Gravador de Macros (Exibir > Macros > Gravar Macro), sem edição no código: `FormatarTratamento_Gravada` seleciona colunas pela Caixa de Nome e aplica AutoAjuste da Largura nas colunas A:T da aba Tratamento. Compare com `FormatarBaseTratada` para mostrar a diferença entre código gravado (`Application.Goto`, `Selection`, referências R1C1) e código escrito.

## Pronto para usar

`01-excel/IngressoData_01_Excel.xlsm` já tem os três módulos e os botões na aba Leia_me. Testado no Excel em 25/11/2026:

| Teste | Resultado |
|---|---|
| RelatorioPeriodo (01/01/2024 a 31/12/2026) | 11 eventos, 2.000 pedidos, 3.804 ingressos, R$ 2.037.612,50, 42,7% turista, ticket R$ 535,65 (igual ao gabarito) |
| RelatorioSemanal / RelatorioDiario | Abas `Rel_Semanal_20260630` e `Rel_Diário_20260630` criadas (último dia com vendas: 30/06/2026) |
| FormatarBaseTratada / FormatarTratamento_Gravada | Rodam sem erro |

Ao abrir o `.xlsm`, clique em **Habilitar Conteúdo** para as macros funcionarem.

## Instalação (refazer a partir do .xlsx)

**Jeito rápido:** em `IngressoData_01_Excel.xlsx`, Alt + F11 > Arquivo > Importar Arquivo: `mdlRelatorioVendas.bas`, `mdlAutomacaoPlanilha.bas` e `mdlMacroGravada.bas`. Depois Alt + F8 > `PrepararPastaComMacros`. O `.xlsm` com botões fica salvo ao lado do `.xlsx`.

**Passo a passo manual:**

1. Abra `IngressoData_01_Excel.xlsx`, pressione **Alt + F11**, **Arquivo > Importar Arquivo** e escolha o `.bas`.
2. Salve como **Pasta de Trabalho Habilitada para Macro (.xlsm)**.
3. **Alt + F8** > `RelatorioSemanal` > Executar. Opcional: inserir botões na aba Leia_me ligados às macros.

Não usa referências externas (sem Scripting.Dictionary), então roda no Excel para Windows e para Mac. Arquivo salvo em ANSI com quebras CRLF para o editor VBA ler os acentos corretamente.
