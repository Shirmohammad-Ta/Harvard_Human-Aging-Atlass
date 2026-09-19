from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from . import models, schemas

# ===== ژن‌ها =====
def get_gene(db: Session, gene_id: int):
    return db.query(models.Gene).filter(models.Gene.gene_id == gene_id).first()

def get_gene_by_symbol(db: Session, symbol: str):
    return db.query(models.Gene).filter(models.Gene.gene_symbol == symbol).first()

def get_genes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Gene).offset(skip).limit(limit).all()

def search_genes(db: Session, query: str, skip: int = 0, limit: int = 20):
    """جستجوی ژن با نماد یا نام یا شناسه"""
    return db.query(models.Gene).filter(
        or_(
            models.Gene.gene_symbol.ilike(f"%{query}%"),
            models.Gene.gene_name.ilike(f"%{query}%"),
            models.Gene.ensembl_id.ilike(f"%{query}%"),
            models.Gene.ncbi_id.ilike(f"%{query}%")
        )
    ).offset(skip).limit(limit).all()

# ===== شواهد =====
def get_evidence_for_gene(db: Session, gene_id: int):
    return db.query(models.GeneEvidence).filter(
        models.GeneEvidence.gene_id == gene_id
    ).all()

def get_evidence_by_layer(db: Session, gene_id: int, layer_id: str):
    return db.query(models.GeneEvidence).filter(
        and_(
            models.GeneEvidence.gene_id == gene_id,
            models.GeneEvidence.layer_id == layer_id
        )
    ).all()

# ===== CpGها =====
def get_cpg_for_gene(db: Session, gene_id: int):
    return db.query(models.CpgSite).filter(
        models.CpgSite.gene_id == gene_id
    ).all()

# ===== پروتئین‌ها =====
def get_proteins_for_gene(db: Session, gene_id: int):
    return db.query(models.Protein).filter(
        models.Protein.gene_id == gene_id
    ).all()  # ✅ اینجا پرانتز بسته شد

# ===== آمار =====
def get_stats(db: Session):
    total_genes = db.query(models.Gene).count()
    total_evidence = db.query(models.GeneEvidence).count()
    layers = {}
    for layer_id in ['GENOMICS', 'EPIGENOMICS', 'TRANSCRIPTOMICS', 'PROTEOMICS']:
        layers[layer_id] = db.query(models.GeneEvidence).filter(
            models.GeneEvidence.layer_id == layer_id
        ).count()
    return {
        "total_genes": total_genes,
        "total_evidence": total_evidence,
        "layers": layers
    }