-- Habilitar extensión pgvector
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE soluciones_ayuda_formacion_es (
    id BIGINT,
    name VARCHAR(255),
    long_description TEXT,
    short_description TEXT,
    web TEXT,
    req_size VARCHAR(255),
    req_tag_title VARCHAR(255),
    req_tag_description VARCHAR(255),
    amount_title_1 VARCHAR(255),
    amount_description_1 VARCHAR(255),
    amount_title_2 VARCHAR(255),
    amount_description_2 VARCHAR(255),
    amount_title_3 VARCHAR(255),
    amount_description_3 VARCHAR(255),
    url_alias VARCHAR(255),
    subsidy_type TEXT,
    origin_types TEXT,
    nombres_areas TEXT,
    nombres_areas_pdf TEXT,
    nombres_areas_boletin TEXT,
    aplicacion_geo TEXT,
    size VARCHAR(255),
    sector_name TEXT,
    sector_specialization_name VARCHAR(255),
    soport_types VARCHAR(255),
    expenses VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);
