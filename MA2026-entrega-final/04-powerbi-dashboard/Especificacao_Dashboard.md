# 04-powerbi-dashboard · Etapa 6: Dashboard Power BI

O `.pbix` só pode ser criado no Power BI Desktop (Windows). Este documento é a especificação para montar o painel em cerca de 1 hora, já com os dados e medidas prontos.

## Montagem

1. **Obter Dados > Excel** e carregar o modelo, ou colar as consultas `.pq` em **Transformar Dados > Nova Fonte > Consulta Nula** (mesmos nomes do Excel).
2. Criar os 4 relacionamentos (ver `03-powerpivot`) e marcar `Dim_Calendario` como tabela de data.
3. Colar as medidas de `medidas.dax` em **Nova Medida**.
4. **Exibir > Temas > Procurar temas** e escolher `IngressoData_tema.json`.
5. Salvar como `IngressoData_Dashboard.pbix` nesta pasta.

## Páginas

**1. Visão Geral**
- Cartões: Faturamento Total, Ingressos Vendidos, Ticket Médio, % Faturamento Turista
- Colunas empilhadas: Faturamento por Categoria × Origem_Publico
- Linha: Faturamento por Dim_Calendario[Ano_Mes]
- Segmentações: Categoria, Praça, Período (Dim_Calendario[Data], entre)

**2. Público Turista** (pergunta central)
- Barras 100% empilhadas: Origem_Publico por Evento
- Mapa (Dim_Praca Latitude/Longitude): bolha = Faturamento Turista
- Tabela: Evento, Faturamento, % Faturamento Turista, % Compradores Turistas, com formatação condicional
- Rosca: Compradores por Dim_Comprador[Tipo_Comprador]

**3. Fatores Externos** (após a Etapa 5)
- Linha com eixo duplo: Ingressos Vendidos e média de Dolar_no_Dia_da_Venda por Ano_Mes
- Dispersão: dólar × ingressos de Turista Internacional por mês
- Colunas: Ingressos em eventos ao ar livre por Condicao_no_Evento
- Cartão: Faturamento Ao Ar Livre

## Regras visuais

- Cores fixas por significado: Local = azul escuro, Turista Nacional = laranja, Turista Internacional = verde. Usar as mesmas cores em todas as páginas.
- No máximo 6 visuais por página; cartões no topo, detalhe embaixo, segmentações à esquerda.
- Títulos dizem a conclusão ("Festivais: 45% da receita vem de turistas"), não só o nome do gráfico.
- Rótulos de dados em reais sem casas decimais; percentuais com 1 casa.
- Contraste mínimo 4,5:1 entre texto e fundo (o tema já respeita).
