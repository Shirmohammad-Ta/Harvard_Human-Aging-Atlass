from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from .. import crud, schemas

router = APIRouter(prefix="/genes", tags=["Genes"])

@router.get("/", response_model=List[schemas.Gene])
def get_genes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    
    return crud.get_genes(db, skip=skip, limit=limit)

@router.get("/{gene_id}", response_model=schemas.Gene)
def get_gene(gene_id: int, db: Session = Depends(get_db)):
    
    gene = crud.get_gene(db, gene_id)
    if not gene:
        raise HTTPException(status_code=404, detail="Gene not found")
    return gene

@router.get("/symbol/{symbol}", response_model=schemas.Gene)
def get_gene_by_symbol(symbol: str, db: Session = Depends(get_db)):
    
    gene = crud.get_gene_by_symbol(db, symbol.upper())
    if not gene:
        raise HTTPException(status_code=404, detail="Gene not found")
    return gene

@router.get("/{gene_id}/evidence", response_model=List[schemas.Evidence])
def get_gene_evidence(
    gene_id: int,
    layer: Optional[str] = None,
    db: Session = Depends(get_db)
):
    
    if layer:
        evidence = crud.get_evidence_by_layer(db, gene_id, layer)
    else:
        evidence = crud.get_evidence_for_gene(db, gene_id)
    return evidence