CREATE TABLE sources (
    source_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    version VARCHAR(20),
    description TEXT,
    url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE evidence_layers (
    layer_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE genes (
    gene_id SERIAL PRIMARY KEY,
    gene_symbol VARCHAR(50) UNIQUE NOT NULL,
    ensembl_id VARCHAR(50),
    ncbi_id VARCHAR(20),
    gene_name TEXT,
    chromosome VARCHAR(10),
    start_position BIGINT,
    end_position BIGINT,
    description TEXT,
    evidence_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE gene_evidence (
    evidence_id SERIAL PRIMARY KEY,
    gene_id INTEGER REFERENCES genes(gene_id) ON DELETE CASCADE,
    layer_id VARCHAR(20) REFERENCES evidence_layers(layer_id),
    source_id VARCHAR(20) REFERENCES sources(source_id),
    evidence_type VARCHAR(50),
    evidence_value TEXT,
    p_value FLOAT,
    fdr FLOAT,
    effect_size FLOAT,
    organ VARCHAR(50),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE cpg_sites (
    cpg_id SERIAL PRIMARY KEY,
    probe_id VARCHAR(50) UNIQUE NOT NULL,
    chromosome VARCHAR(10),
    position BIGINT,
    gene_id INTEGER REFERENCES genes(gene_id) ON DELETE SET NULL,
    tss_distance INTEGER,
    annotation_method VARCHAR(50),
    beta_value FLOAT,
    p_value FLOAT,
    source VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE proteins (
    protein_id SERIAL PRIMARY KEY,
    uniprot_id VARCHAR(20) UNIQUE,
    gene_id INTEGER REFERENCES genes(gene_id) ON DELETE CASCADE,
    assay_target VARCHAR(100),
    platform VARCHAR(50),
    organ VARCHAR(50),
    coefficient FLOAT,
    selection_frequency FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE data_version (
    version_id SERIAL PRIMARY KEY,
    version_tag VARCHAR(50) UNIQUE NOT NULL,
    source_checksum VARCHAR(64),
    total_genes INTEGER,
    total_evidence INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);


CREATE INDEX idx_genes_symbol ON genes(gene_symbol);
CREATE INDEX idx_genes_ensembl ON genes(ensembl_id);
CREATE INDEX idx_evidence_gene ON gene_evidence(gene_id);
CREATE INDEX idx_evidence_layer ON gene_evidence(layer_id);
CREATE INDEX idx_cpg_gene ON cpg_sites(gene_id);
CREATE INDEX idx_protein_gene ON proteins(gene_id);


INSERT INTO evidence_layers (layer_id, name, description) VALUES
('GENOMICS', 'Genomics', 'Genetic and lifespan evidence from GenAge and LongevityMap'),
('EPIGENOMICS', 'Epigenomics', 'DNA methylation age evidence from cAge and bAge'),
('TRANSCRIPTOMICS', 'Transcriptomics', 'Gene expression age evidence from tAge'),
('PROTEOMICS', 'Proteomics', 'Protein-level age evidence from OrganAge');

INSERT INTO sources (source_id, name, version, description) VALUES
('GENAGE', 'GenAge', '2024', 'Human aging gene database'),
('LONGEVITYMAP', 'LongevityMap', '2023', 'Human longevity associations'),
('CAGE', 'cAge', '2023', 'Chronological age CpGs'),
('BAGE', 'bAge', '2023', 'All-cause mortality CpGs'),
('TAGE', 'tAge', '2026', 'Transcriptomic age signatures');