import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from pathlib import Path
import os


DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'human_aging_atlass',
    'user': 'atlas_user',
    'password': 'Harvard123'
}

def load_genes(conn):
    
    df = pd.read_parquet('data/parquet/genes.parquet')
    
    # تطابق ستون‌ها با اسکیما
    df = df.rename(columns={
        'gene_symbol': 'gene_symbol',
        'ensembl_id': 'ensembl_id',
        'ncbi_id': 'ncbi_id',
        'gene_name': 'gene_name',
        'evidence_reason': 'evidence_reason'
    })
    
    # پر کردن مقادیر خالی
    df = df.fillna({
        'ensembl_id': 'Unknown',
        'ncbi_id': 'Unknown',
        'gene_name': 'Unknown',
        'evidence_reason': 'Unknown'
    })
    
    cursor = conn.cursor()
    
    # حذف داده‌های قبلی
    cursor.execute("TRUNCATE genes RESTART IDENTITY CASCADE;")
    
    # بارگذاری با execute_values
    data = df[['gene_symbol', 'ensembl_id', 'ncbi_id', 'gene_name', 'evidence_reason']].values.tolist()
    execute_values(
        cursor,
        """
        INSERT INTO genes (gene_symbol, ensembl_id, ncbi_id, gene_name, evidence_reason)
        VALUES %s
        """,
        data
    )
    
    conn.commit()
    print(f" Loaded {len(df)} genes into PostgreSQL")

def load_sources_and_layers(conn):
    """بارگذاری جداول منابع و لایه‌ها"""
    cursor = conn.cursor()
    
    # بارگذاری لایه‌ها
    layers = [
        ('GENOMICS', 'Genomics', 'Genetic and lifespan evidence'),
        ('EPIGENOMICS', 'Epigenomics', 'DNA methylation age evidence'),
        ('TRANSCRIPTOMICS', 'Transcriptomics', 'Gene expression age evidence'),
        ('PROTEOMICS', 'Proteomics', 'Protein-level age evidence')
    ]
    execute_values(
        cursor,
        "INSERT INTO evidence_layers (layer_id, name, description) VALUES %s ON CONFLICT (layer_id) DO NOTHING",
        layers
    )
    
    # بارگذاری منابع
    sources = [
        ('GENAGE', 'GenAge', '2024', 'Human aging gene database'),
        ('LONGEVITYMAP', 'LongevityMap', '2023', 'Human longevity associations'),
        ('CAGE', 'cAge', '2023', 'Chronological age CpGs'),
        ('BAGE', 'bAge', '2023', 'All-cause mortality CpGs'),
        ('TAGE', 'tAge', '2026', 'Transcriptomic age signatures')
    ]
    execute_values(
        cursor,
        "INSERT INTO sources (source_id, name, version, description) VALUES %s ON CONFLICT (source_id) DO NOTHING",
        sources
    )
    
    conn.commit()
    print("✅ Loaded sources and layers")

def main():
    print("🚀 Loading data to PostgreSQL...")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Connected to PostgreSQL")
        
        load_sources_and_layers(conn)
        load_genes(conn)
        
        # نمایش آمار
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM genes")
        gene_count = cursor.fetchone()[0]
        print(f"📊 Total genes in database: {gene_count}")
        
        cursor.execute("SELECT COUNT(*) FROM evidence_layers")
        layer_count = cursor.fetchone()[0]
        print(f"📊 Total layers: {layer_count}")
        
        cursor.execute("SELECT COUNT(*) FROM sources")
        source_count = cursor.fetchone()[0]
        print(f"📊 Total sources: {source_count}")
        
        conn.close()
        print("\n✅ All data loaded successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()