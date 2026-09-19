import pandas as pd
import requests
import json
import time
from pathlib import Path

def normalize_gene_identifiers(df, symbol_column='gene_symbol'):
    """
    Attach Ensembl ID and validate HGNC symbols using MyGene.info API
    """
    def get_gene_info(symbol):
        try:
            url = f"http://mygene.info/v3/query?q={symbol}&species=human&fields=ensembl,entrez"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                
                if isinstance(data, dict) and data.get("hits"):
                    hit = data["hits"][0]
                    
                    if isinstance(hit, dict):
                        return {
                            'ensembl_id': hit.get('ensembl', {}).get('gene') if isinstance(hit.get('ensembl'), dict) else None,
                            'validated_ncbi': str(hit.get('entrez', '')) if hit.get('entrez') else None
                        }
                
                
                print(f"⚠️ Unexpected response format for {symbol}: {type(data)}")
                return {'ensembl_id': None, 'validated_ncbi': None}
                
        except Exception as e:
            print(f"⚠️ Error for {symbol}: {e}")
        return {'ensembl_id': None, 'validated_ncbi': None}
    
   
    gene_info_list = []
    symbols = df[symbol_column].unique()
    total = len(symbols)
    
    for i, symbol in enumerate(symbols):
        print(f"  🔍 Processing {symbol} ({i+1}/{total})...")
        info = get_gene_info(symbol)
        info['symbol'] = symbol
        gene_info_list.append(info)
        time.sleep(0.5)  
    
    
    info_df = pd.DataFrame(gene_info_list)
    df = df.merge(info_df, left_on=symbol_column, right_on='symbol', how='left')
    
    return df

def normalize_genes(parquet_path, output_path):
    """
    Normalize gene identifiers and create master gene table
    """
    
    df = pd.read_parquet(parquet_path)
    
    print(f"🔄 Normalizing {len(df)} genes...")
    
    
    df = normalize_gene_identifiers(df)
    
    
    gene_table = df[[
        'gene_symbol',
        'ensembl_id',
        'ncbi_id',
        'validated_ncbi',
        'gene_name',
        'evidence_reason'
    ]].drop_duplicates(subset=['gene_symbol'])
    
    
    gene_table = gene_table.dropna(subset=['gene_symbol'])
    
    
    gene_table = gene_table.fillna({
        'ensembl_id': 'Unknown',
        'validated_ncbi': 'Unknown'
    })
    
    
    gene_table.to_parquet(output_path, index=False)
    
    print(f"✅ Gene table saved to {output_path} with {len(gene_table)} genes")
    return gene_table

if __name__ == "__main__":
    parquet_file = Path("data/parquet/genage.parquet")
    gene_file = Path("data/parquet/genes.parquet")
    
    normalize_genes(parquet_file, gene_file)