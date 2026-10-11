# Relatório Parcial · IngressoData Brasil

Microinformática Aplicada (ILP590) · FATEC SP · Prof. Veríssimo · 2º/2026
Entrega parcial: Etapa 1 (Excel Avançado + Power Query) e Etapa 2 (Power Pivot + DAX)

## 1. Objetivo da entrega

Transformar planilhas brutas de vendas de ingressos, espalhadas por praça e sem padrão, em uma base única e confiável, e responder a primeira parte da pergunta central: quanto do faturamento vem do público turista em cada tipo de evento.

## 2. Base de dados

Três arquivos simulados, um por praça, cada um com um "jeito" diferente de registrar:

| Arquivo | Formato | Particularidades |
|---|---|---|
| vendas_SP.xlsx | Excel | datas e valores como texto ("15/03/2025", "R$ 1.250,00") |
| vendas_RJ.xlsx | Excel | datas e valores numéricos |
| vendas_MG.csv | CSV (;) | datas "2025-03-15", decimal com vírgula |

Problemas inseridos de propósito: categorias e cidades com grafias diferentes (SHOW, Shows, Fest., Cine, BH, Sao Paulo, SP - São Paulo), país escrito de 4 formas, 49 duplicadas, 12 linhas vazias e 30 vendas sem quantidade ou valor.

## 3. Etapa 1: Excel Avançado

A aba **Tratamento** limpa a base só com fórmulas, sem mexer no dado bruto:

- datas: identifica o formato e converte com DATA/EXT.TEXTO;
- valores: VALORNUMERO, que independe do idioma do Excel;
- padronização: PROCX sobre tabelas De-Para editáveis;
- duplicadas: CONT.SE acumulado no ID_Venda;
- origem do público: Local (mora na cidade-sede), Turista Nacional ou Turista Internacional.

A aba **Auditoria** prova que nenhuma linha some sem motivo: 2.091 brutas = 12 vazias + 49 duplicadas + 30 inválidas + **2.000 válidas**, com 0 erros de fórmula e 0 valores sem De-Para.

## 4. Etapa 1: Power Query

As mesmas regras em linguagem M, lendo os três arquivos direto da pasta. Funções reutilizáveis (fnTratarData, fnTratarNumero, fnLerAba), De-Para em tabela externa e consolidação com Table.Combine. Resultado idêntico ao Excel: 2.000 linhas e R$ 2.037.612,50.

## 5. Etapa 2: Power Pivot e DAX

Star Schema com a fato **Fato_Vendas_Ingressos** e as dimensões **Dim_Evento**, **Dim_Praca**, **Dim_Comprador** e **Dim_Calendario**. Medidas principais: Faturamento Total, Ingressos Vendidos, Ticket Médio, Faturamento Turista, % Faturamento Turista, % Compradores Turistas, Participação Categoria e Variação Mensal %.

## 6. Resultados preliminares

| Categoria | Faturamento | Ingressos | Ticket médio | % faturamento turista | Participação |
|---|---:|---:|---:|---:|---:|
| Festival | R$ 1.460.022,50 | 1725 | R$ 846,39 | 45,0% | 71,7% |
| Show | R$ 548.412,50 | 1155 | R$ 474,82 | 38,8% | 26,9% |
| Cinema | R$ 29.177,50 | 924 | R$ 31,58 | 6,0% | 1,4% |
| **Total** | **R$ 2.037.612,50** | **3804** | **R$ 535,65** | **42,7%** | **100%** |
- **42,7% do faturamento vem de turistas.** Nos festivais chega a 45%; no cinema é só 6%, um público essencialmente local.
- Festivais concentram 71,7% da receita com 45% dos ingressos: são o produto mais sensível ao turismo.
- 58,7% dos compradores fizeram ao menos uma compra como turista.
- A influência do dólar e do clima entra na entrega final (Etapa 5, APIs do Banco Central e Open-Meteo).

## 7. Validação

Os números foram conferidos em três caminhos independentes (fórmulas do Excel, script Python de referência e consultas SQL) e batem centavo a centavo. Gabarito em `03-powerpivot/gabarito.json`.

## 8. Próximas etapas

VBA (relatórios automáticos) → SQL (DDL/DML) → APIs de câmbio e clima → Dashboard Power BI. Os artefatos já estão adiantados em `MA2026-entrega-final`.
