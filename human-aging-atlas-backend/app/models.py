from sqlalchemy import Column, Integer, String, Text, Float, BigInteger, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Gene(Base):
    __tablename__ = "genes"

    gene_id = Column(Integer, primary_key=True, index=True)
    gene_symbol = Column(String(50), unique=True, nullable=False, index=True)
    ensembl_id = Column(String(50))
    ncbi_id = Column(String(20))
    gene_name = Column(Text)
    chromosome = Column(String(10))
    start_position = Column(BigInteger)
    end_position = Column(BigInteger)
    description = Column(Text)
    evidence_reason = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    evidence = relationship("GeneEvidence", back_populates="gene")
    cpg_sites = relationship("CpgSite", back_populates="gene")
    proteins = relationship("Protein", back_populates="gene")

class GeneEvidence(Base):
    __tablename__ = "gene_evidence"

    evidence_id = Column(Integer, primary_key=True, index=True)
    gene_id = Column(Integer, ForeignKey("genes.gene_id", ondelete="CASCADE"))
    layer_id = Column(String(20), ForeignKey("evidence_layers.layer_id"))
    source_id = Column(String(20), ForeignKey("sources.source_id"))
    evidence_type = Column(String(50))
    evidence_value = Column(Text)
    p_value = Column(Float)
    fdr = Column(Float)
    effect_size = Column(Float)
    organ = Column(String(50))
    meta_data = Column(JSON)  # ✅ تغییر نام
    created_at = Column(TIMESTAMP, server_default=func.now())

    gene = relationship("Gene", back_populates="evidence")

class CpgSite(Base):
    __tablename__ = "cpg_sites"

    cpg_id = Column(Integer, primary_key=True, index=True)
    probe_id = Column(String(50), unique=True, nullable=False)
    chromosome = Column(String(10))
    position = Column(BigInteger)
    gene_id = Column(Integer, ForeignKey("genes.gene_id", ondelete="SET NULL"))
    tss_distance = Column(Integer)
    annotation_method = Column(String(50))
    beta_value = Column(Float)
    p_value = Column(Float)
    source = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())

    gene = relationship("Gene", back_populates="cpg_sites")

class Protein(Base):
    __tablename__ = "proteins"

    protein_id = Column(Integer, primary_key=True, index=True)
    uniprot_id = Column(String(20), unique=True)
    gene_id = Column(Integer, ForeignKey("genes.gene_id", ondelete="CASCADE"))
    assay_target = Column(String(100))
    platform = Column(String(50))
    organ = Column(String(50))
    coefficient = Column(Float)
    selection_frequency = Column(Float)
    created_at = Column(TIMESTAMP, server_default=func.now())

    gene = relationship("Gene", back_populates="proteins")