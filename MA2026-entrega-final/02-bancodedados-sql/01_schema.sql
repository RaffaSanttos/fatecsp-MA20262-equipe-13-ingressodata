-- IngressoData Brasil — Etapa 4: Modelagem do banco relacional (DDL)
-- Compatível com SQLite 3 e PostgreSQL 13+. Ordem de execução: 01_schema -> 02_carga_dados -> 03_consultas

DROP TABLE IF EXISTS fato_vendas_ingressos;
DROP TABLE IF EXISTS dim_comprador;
DROP TABLE IF EXISTS dim_evento;
DROP TABLE IF EXISTS dim_praca;

CREATE TABLE dim_praca (
    cidade      VARCHAR(60)  PRIMARY KEY,
    uf          CHAR(2)      NOT NULL,
    regiao      VARCHAR(20)  NOT NULL,
    latitude    DECIMAL(9,6) NOT NULL,
    longitude   DECIMAL(9,6) NOT NULL
);

CREATE TABLE dim_evento (
    evento        VARCHAR(80) PRIMARY KEY,
    categoria     VARCHAR(20) NOT NULL CHECK (categoria IN ('Show', 'Festival', 'Cinema')),
    cidade_evento VARCHAR(60) NOT NULL REFERENCES dim_praca (cidade),
    local_evento  VARCHAR(80) NOT NULL,
    ao_ar_livre   VARCHAR(3)  NOT NULL CHECK (ao_ar_livre IN ('Sim', 'Não')),
    data_evento   DATE        -- vazio para cinema (sessões diárias)
);

CREATE TABLE dim_comprador (
    comprador_id   VARCHAR(10) PRIMARY KEY,
    cidade         VARCHAR(60) NOT NULL,
    uf             VARCHAR(2)  NOT NULL,
    pais           VARCHAR(30) NOT NULL,
    tipo_comprador VARCHAR(12) NOT NULL CHECK (tipo_comprador IN ('Nacional', 'Estrangeiro'))
);

CREATE TABLE fato_vendas_ingressos (
    id_venda       VARCHAR(12)   PRIMARY KEY,
    data_venda     DATE          NOT NULL,
    data_evento    DATE          NOT NULL,
    evento         VARCHAR(80)   NOT NULL REFERENCES dim_evento (evento),
    categoria      VARCHAR(20)   NOT NULL,
    cidade_evento  VARCHAR(60)   NOT NULL REFERENCES dim_praca (cidade),
    tipo_ingresso  VARCHAR(10)   NOT NULL,
    qtd            INTEGER       NOT NULL CHECK (qtd > 0),
    valor_unitario DECIMAL(10,2) NOT NULL CHECK (valor_unitario > 0),
    valor_total    DECIMAL(12,2) NOT NULL,
    canal          VARCHAR(15)   NOT NULL,
    comprador_id   VARCHAR(10)   NOT NULL REFERENCES dim_comprador (comprador_id),
    origem_publico VARCHAR(25)   NOT NULL CHECK (origem_publico IN ('Local', 'Turista Nacional', 'Turista Internacional')),
    arquivo_origem VARCHAR(20)   NOT NULL,
    CHECK (data_venda <= data_evento)
);

CREATE INDEX idx_fato_data_venda ON fato_vendas_ingressos (data_venda);
CREATE INDEX idx_fato_evento ON fato_vendas_ingressos (evento);
CREATE INDEX idx_fato_origem ON fato_vendas_ingressos (origem_publico);
