# 01-vba · Etapa 3: Automação com macros

`mdlRelatorioVendas.bas` gera relatórios de vendas por evento e praça a partir da tabela `tbVendasTratadas` (planilha do 01-excel).

| Macro | O que faz |
|---|---|
| RelatorioDiario | Vendas do último dia com movimento |
| RelatorioSemanal | Últimos 7 dias |
| RelatorioPeriodo | Pede data inicial e final |
| AtualizarDados | Atualiza Power Query e modelo (Atualizar Tudo) |

Cada relatório cria a aba `Rel_<tipo>_<aaaammdd>` com pedidos, ingressos, faturamento, faturamento turista, % turista e ticket médio, ordenada por faturamento.

## Instalação

1. Abra `IngressoData_01_Excel.xlsx`, pressione **Alt + F11**, **Arquivo > Importar Arquivo** e escolha o `.bas`.
2. Salve como **Pasta de Trabalho Habilitada para Macro (.xlsm)**.
3. **Alt + F8** > `RelatorioSemanal` > Executar. Opcional: inserir botões na aba Leia_me ligados às macros.

Não usa referências externas (sem Scripting.Dictionary), então roda no Excel para Windows e para Mac. Arquivo salvo em ANSI com quebras CRLF para o editor VBA ler os acentos corretamente.
