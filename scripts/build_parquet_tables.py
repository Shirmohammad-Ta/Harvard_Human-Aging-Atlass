import pandas as pd
import json
from pathlib import Path
from datetime import datetime

def build_parquet_tables():
    """
    Master script to build all Parquet tables
    """
    print("🏗️ Building Human Aging Atlas Parquet tables...")
    
    
    Path("data/parquet").mkdir(parents=True, exist_ok=True)
    
    
    from extract_genage import extract_genage
    genage_df = extract_genage(
        Path("data/raw/genage_human.csv"),
        Path("data/parquet/genage.parquet")
    )
    
    
    from normalize_genes import normalize_genes
    genes_df = normalize_genes(
        Path("data/parquet/genage.parquet"),
        Path("data/parquet/genes.parquet")
    )
    
    
    sources_df = pd.DataFrame([
        {'source_id': 'GENAGE', 'name': 'GenAge', 'version': '2024', 'description': 'Human aging gene database'},
        {'source_id': 'LONGEVITYMAP', 'name': 'LongevityMap', 'version': '2023', 'description': 'Human longevity associations'},
        {'source_id': 'CAGE', 'name': 'cAge', 'version': '2023', 'description': 'Chronological age CpGs'},
        {'source_id': 'BAGE', 'name': 'bAge', 'version': '2023', 'description': 'All-cause mortality CpGs'},
        {'source_id': 'TAGE', 'name': 'tAge', 'version': '2026', 'description': 'Transcriptomic age signatures'}
    ])
    sources_df.to_parquet("data/parquet/sources.parquet", index=False)
    
    
    layers_df = pd.DataFrame([
        {'layer_id': 'GENOMICS', 'name': 'Genomics', 'description': 'Genetic and lifespan evidence'},
        {'layer_id': 'EPIGENOMICS', 'name': 'Epigenomics', 'description': 'DNA methylation age evidence'},
        {'layer_id': 'TRANSCRIPTOMICS', 'name': 'Transcriptomics', 'description': 'Gene expression age evidence'},
        {'layer_id': 'PROTEOMICS', 'name': 'Proteomics', 'description': 'Protein-level age evidence'}
    ])
    layers_df.to_parquet("data/parquet/evidence_layers.parquet", index=False)
    
    
    report = {
        'build_timestamp': datetime.now().isoformat(),
        'total_genes': len(genes_df),
        'sources': sources_df.to_dict('records'),
        'layers': layers_df.to_dict('records'),
        'source_files': {
            'genage': str(Path("data/raw/genage_human.csv").exists()),
        }
    }
    
    with open("data/parquet/build_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("\n✅ All Parquet tables built successfully!")
    print(f"📊 Genes: {len(genes_df)}")
    print(f"📁 Output: data/parquet/")
    
    return genes_df

if __name__ == "__main__":
    build_parquet_tables()