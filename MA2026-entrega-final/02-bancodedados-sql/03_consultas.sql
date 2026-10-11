-- IngressoData Brasil — Etapa 4: Consultas analíticas (DML)
-- Portáveis entre SQLite e PostgreSQL (datas guardadas em formato ISO aaaa-mm-dd).

-- Q1. KPIs por categoria: faturamento, ingressos, ticket médio, % turista e participação
SELECT
    categoria,
    SUM(valor_total)                                                    AS faturamento,
    SUM(qtd)                                                            AS ingressos,
    ROUND(SUM(valor_total) / SUM(qtd), 2)                               AS ticket_medio,
    ROUND(100.0 * SUM(CASE WHEN origem_publico <> 'Local' THEN valor_total ELSE 0 END)
          / SUM(valor_total), 2)                                        AS pct_faturamento_turista,
    ROUND(100.0 * SUM(valor_total)
          / (SELECT SUM(valor_total) FROM fato_vendas_ingressos), 2)   AS pct_participacao
FROM fato_vendas_ingressos
GROUP BY categoria
ORDER BY faturamento DESC;

-- Q2. Pergunta central: participação do público turista no faturamento por tipo de evento
SELECT
    categoria,
    origem_publico,
    SUM(valor_total) AS faturamento,
    ROUND(100.0 * SUM(valor_total)
          / SUM(SUM(valor_total)) OVER (PARTITION BY categoria), 2) AS pct_dentro_da_categoria
FROM fato_vendas_ingressos
GROUP BY categoria, origem_publico
ORDER BY categoria, faturamento DESC;

-- Q3. Ranking de eventos por faturamento com % de compradores turistas (JOIN com dimensão)
SELECT
    e.evento,
    e.categoria,
    e.cidade_evento,
    e.ao_ar_livre,
    SUM(f.valor_total)                                                        AS faturamento,
    COUNT(DISTINCT f.comprador_id)                                            AS compradores,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN f.origem_publico <> 'Local' THEN f.comprador_id END)
          / COUNT(DISTINCT f.comprador_id), 2)                                AS pct_compradores_turistas
FROM fato_vendas_ingressos f
JOIN dim_evento e ON e.evento = f.evento
GROUP BY e.evento, e.categoria, e.cidade_evento, e.ao_ar_livre
ORDER BY faturamento DESC;

-- Q4. Evolução mensal de vendas (base para cruzar com cotação do dólar)
SELECT
    SUBSTR(CAST(data_venda AS VARCHAR(10)), 1, 7)                             AS ano_mes,
    SUM(qtd)                                                                  AS ingressos,
    SUM(valor_total)                                                          AS faturamento,
    SUM(CASE WHEN origem_publico = 'Turista Internacional' THEN qtd ELSE 0 END) AS ingressos_estrangeiros
FROM fato_vendas_ingressos
GROUP BY SUBSTR(CAST(data_venda AS VARCHAR(10)), 1, 7)
ORDER BY ano_mes;

-- Q5. Faturamento por praça e origem do público
SELECT
    p.cidade,
    p.uf,
    SUM(CASE WHEN f.origem_publico = 'Local' THEN f.valor_total ELSE 0 END)                 AS local,
    SUM(CASE WHEN f.origem_publico = 'Turista Nacional' THEN f.valor_total ELSE 0 END)      AS turista_nacional,
    SUM(CASE WHEN f.origem_publico = 'Turista Internacional' THEN f.valor_total ELSE 0 END) AS turista_internacional,
    SUM(f.valor_total)                                                                      AS total
FROM fato_vendas_ingressos f
JOIN dim_praca p ON p.cidade = f.cidade_evento
GROUP BY p.cidade, p.uf
ORDER BY total DESC;

-- Q6. Vendas de última hora (mesma data do evento) em eventos ao ar livre
SELECT
    f.evento,
    f.data_evento,
    SUM(f.qtd) AS ingressos_no_dia
FROM fato_vendas_ingressos f
JOIN dim_evento e ON e.evento = f.evento
WHERE e.ao_ar_livre = 'Sim'
  AND f.data_venda = f.data_evento
GROUP BY f.evento, f.data_evento
ORDER BY ingressos_no_dia DESC;

-- Q7. Canais de venda e ticket médio por tipo de ingresso
SELECT
    canal,
    tipo_ingresso,
    COUNT(*)                                AS pedidos,
    ROUND(SUM(valor_total) / SUM(qtd), 2)   AS ticket_medio
FROM fato_vendas_ingressos
GROUP BY canal, tipo_ingresso
ORDER BY canal, ticket_medio DESC;

-- Q8. View com os KPIs gerais (usada pelo Power BI se ligado ao banco)
DROP VIEW IF EXISTS vw_kpis_gerais;
CREATE VIEW vw_kpis_gerais AS
SELECT
    SUM(valor_total)                                                                  AS faturamento_total,
    SUM(qtd)                                                                          AS ingressos_vendidos,
    COUNT(*)                                                                          AS pedidos,
    ROUND(SUM(valor_total) / SUM(qtd), 2)                                             AS ticket_medio,
    ROUND(100.0 * SUM(CASE WHEN origem_publico <> 'Local' THEN valor_total ELSE 0 END)
          / SUM(valor_total), 2)                                                      AS pct_faturamento_turista
FROM fato_vendas_ingressos;

SELECT * FROM vw_kpis_gerais;
