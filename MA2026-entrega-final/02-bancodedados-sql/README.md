# 02-bancodedados-sql · Etapa 4: Banco relacional (DDL e DML)

Rodar na ordem. Compatível com **SQLite 3** (DB Browser for SQLite) e **PostgreSQL 13+** (pgAdmin).

| Arquivo | Conteúdo |
|---|---|
| `01_schema.sql` | DDL: 4 tabelas com chaves primárias, estrangeiras, CHECKs e índices |
| `02_carga_dados.sql` | DML: carga das 2.000 vendas e das dimensões (gerada da base tratada) |
| `03_consultas.sql` | 7 consultas analíticas + view `vw_kpis_gerais` |

## Consultas

| Nº | Pergunta |
|---|---|
| Q1 | KPIs por categoria (faturamento, ticket médio, % turista, participação) |
| Q2 | Pergunta central: participação de cada origem de público por categoria (função de janela) |
| Q3 | Ranking de eventos com % de compradores turistas (JOIN com Dim_Evento) |
| Q4 | Evolução mensal: base para cruzar com o dólar |
| Q5 | Faturamento por praça e origem |
| Q6 | Vendas de última hora em eventos ao ar livre: base para cruzar com o clima |
| Q7 | Canal × tipo de ingresso |
| Q8 | View de KPIs gerais |

Testado: os 3 scripts rodam no SQLite sem erro e sem violação de chave estrangeira, e os totais batem com o Excel (R$ 2.037.612,50; 42,74% turista). A sintaxe também foi validada com o parser oficial do PostgreSQL (pglast).
