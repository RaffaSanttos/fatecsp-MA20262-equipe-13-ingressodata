# 02-powerquery · Etapa 1: Power Query (linguagem M)

Automatiza a mesma limpeza da aba Tratamento, lendo direto os arquivos de `01-excel/dados-brutos/`.

## Como montar no Excel (Windows: Dados > Obter Dados > Iniciar Editor do Power Query)

1. Para cada arquivo `.pq`, em ordem numérica: **Nova Fonte > Outras Fontes > Consulta Nula**, abra o **Editor Avançado**, apague o conteúdo e cole o arquivo.
2. Renomeie a consulta com o nome do arquivo **sem o número e sem o .pq** (ex.: `01_fnTratarData.pq` vira `fnTratarData`). Os nomes precisam ser exatos porque as consultas se referenciam.
3. Em `pPastaDados`, troque o caminho pela pasta `dados-brutos` no seu computador (terminando com `\`).
4. **Fechar e Carregar Para...**: `Fato_Vendas_Ingressos` e as 4 `Dim_*` como **Somente Conexão + Adicionar ao Modelo de Dados**. As demais como Somente Conexão.

| Consulta | Papel |
|---|---|
| pPastaDados | Parâmetro com a pasta dos arquivos |
| fnTratarData / fnTratarNumero | Funções que convertem os 3 formatos de data e os valores em texto |
| fnLerAba | Lê uma aba de um .xlsx da pasta |
| DePara_Categoria / Cidade / Pais | Tabelas de padronização (de `tabelas_apoio.xlsx`) |
| Vendas_SP / Vendas_RJ / Vendas_MG | Fontes brutas (2 Excel + 1 CSV) |
| Fato_Vendas_Ingressos | Empilha, remove vazias e duplicadas, padroniza, valida e classifica o público |
| Dim_Evento / Dim_Praca / Dim_Comprador / Dim_Calendario | Dimensões do Star Schema |

## Conferência depois de carregar

`Fato_Vendas_Ingressos` deve ter **2.000 linhas** e somar **R$ 2.037.612,50** em `Valor_Total`. Dimensões: 11 eventos, 3 praças, 932 compradores, 730 dias. Se bater, o Power Query está idêntico ao Excel.

Sintaxe de todos os arquivos validada com o parser oficial da Microsoft (`@microsoft/powerquery-parser`).
