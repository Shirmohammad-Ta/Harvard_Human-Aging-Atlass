from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class GeneBase(BaseModel):
    gene_symbol: str
    ensembl_id: Optional[str] = None
    ncbi_id: Optional[str] = None
    gene_name: Optional[str] = None
    chromosome: Optional[str] = None
    start_position: Optional[int] = None
    end_position: Optional[int] = None
    description: Optional[str] = None
    evidence_reason: Optional[str] = None

class GeneCreate(GeneBase):
    pass

class Gene(GeneBase):
    gene_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EvidenceBase(BaseModel):
    layer_id: str
    source_id: str
    evidence_type: Optional[str] = None
    evidence_value: Optional[str] = None
    p_value: Optional[float] = None
    fdr: Optional[float] = None
    effect_size: Optional[float] = None
    organ: Optional[str] = None
    meta_data: Optional[dict] = None

class Evidence(EvidenceBase):
    evidence_id: int
    gene_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class SearchResult(BaseModel):
    gene: Gene
    evidence: List[Evidence]
    cpg_sites: List[dict]
    proteins: List[dict]


class StatsResponse(BaseModel):
    total_genes: int
    total_evidence: int
    layers: dict
    sources: dict
    chromosomes: dict