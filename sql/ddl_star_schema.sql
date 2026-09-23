-- =============================================================================
-- PROJETO: Pipeline Lakehouse de Indicadores Operacionais & KPIs de Frota
-- CAMADA: Gold (Star Schema - Kimball)
-- ARQUIVO: ddl_star_schema.sql
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. Tabela Dimensão Equipamento
-- -----------------------------------------------------------------------------
CREATE TABLE dim_equipamento (
    sk_equipamento INT PRIMARY KEY,
    id_ativo VARCHAR(50) NOT NULL,
    categoria_equipamento VARCHAR(100) NOT NULL,
    filial_operacao VARCHAR(100) NOT NULL
);

-- -----------------------------------------------------------------------------
-- 2. Tabela Dimensão Tempo / Calendário
-- -----------------------------------------------------------------------------
CREATE TABLE dim_tempo (
    sk_tempo INT PRIMARY KEY, -- Formato YYYYMMDD
    data DATE NOT NULL,
    ano INT NOT NULL,
    mes INT NOT NULL,
    nome_mes VARCHAR(20) NOT NULL,
    trimestre INT NOT NULL,
    dia_semana VARCHAR(20) NOT NULL
);

-- -----------------------------------------------------------------------------
-- 3. Tabela Fato Chamados de Manutenção & Operação
-- -----------------------------------------------------------------------------
CREATE TABLE fato_chamados (
    id_chamado VARCHAR(50) PRIMARY KEY,
    sk_equipamento INT NOT NULL,
    sk_tempo INT NOT NULL,
    dt_abertura_chamado TIMESTAMP NOT NULL,
    dt_conclusao_chamado TIMESTAMP NOT NULL,
    sla_prometido_horas INT NOT NULL,
    tempo_atendimento_horas DECIMAL(10, 1) NOT NULL,
    custo_manutencao DECIMAL(12, 2) NOT NULL,
    fl_estourou_sla INT NOT NULL, -- 0 = Dentro do Prazo, 1 = Estourou SLA
    horas_atraso DECIMAL(10, 1) NOT NULL,
    status_ativo VARCHAR(50) NOT NULL,
    
    -- Chaves Estrangeiras (Foreign Keys)
    CONSTRAINT fk_fato_equipamento FOREIGN KEY (sk_equipamento) REFERENCES dim_equipamento(sk_equipamento),
    CONSTRAINT fk_fato_tempo FOREIGN KEY (sk_tempo) REFERENCES dim_tempo(sk_tempo)
);