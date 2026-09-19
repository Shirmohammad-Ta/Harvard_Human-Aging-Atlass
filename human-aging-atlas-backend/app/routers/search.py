from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import crud, schemas

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/", response_model=List[schemas.Gene])
def search_genes(
    q: str = Query(..., min_length=2, description="Search keywords"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    
    return crud.search_genes(db, q, skip=skip, limit=limit)

@router.get("/full/{symbol}", response_model=schemas.SearchResult)
def get_full_gene_info(symbol: str, db: Session = Depends(get_db)):
    
    gene = crud.get_gene_by_symbol(db, symbol.upper())
    if not gene:
        raise HTTPException(status_code=404, detail="Gene not found")
    
    evidence = crud.get_evidence_for_gene(db, gene.gene_id)
    cpg_sites = crud.get_cpg_for_gene(db, gene.gene_id)
    proteins = crud.get_proteins_for_gene(db, gene.gene_id)
    
    return {
        "gene": gene,
        "evidence": evidence,
        "cpg_sites": cpg_sites,
        "proteins": proteins
    }