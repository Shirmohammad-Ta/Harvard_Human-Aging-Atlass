import pandas as pd
import requests
import time
from pathlib import Path

def extract_genage(raw_path, output_path):
    """
    Extract GenAge data and normalize to Parquet format
    """
    
    df = pd.read_csv(raw_path)
    
    print(f"✅ GenAge: {len(df)} rows loaded")
    
    
    normalized = df.rename(columns={
        'symbol': 'gene_symbol',
        'entrez gene id': 'ncbi_id',
        'name': 'gene_name',
        'why': 'evidence_reason'
    })
    
    # اضافه کردن متادیتا
    normalized['source'] = 'GenAge'
    normalized['source_version'] = '2024'
    normalized['species'] = 'human'
    
    
    normalized = normalized.dropna(subset=['gene_symbol'])
    normalized = normalized[normalized['gene_symbol'].str.strip() != '']
    
    
    normalized.to_parquet(output_path, index=False)
    
    print(f"✅ GenAge saved to {output_path} with {len(normalized)} genes")
    return normalized

if __name__ == "__main__":
    raw_file = Path("data/raw/genage_human.csv")
    parquet_file = Path("data/parquet/genage.parquet")
    
    extract_genage(raw_file, parquet_file)