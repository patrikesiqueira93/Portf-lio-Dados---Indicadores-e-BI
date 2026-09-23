import sys
import subprocess
import os
from datetime import datetime

# Garante que o pyarrow está instalado para suporte ao formato Parquet
try:
    import pyarrow
except ImportError:
    print("📦 Dependência 'pyarrow' não encontrada. Instalando automaticamente...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyarrow"])
    import pyarrow

import pandas as pd

def executar_ingestao_bronze():
    print("🚀 Iniciando ingestão da Camada Bronze...")
    
    # Descobre a pasta raiz do projeto automaticamente (uma pasta acima de /notebooks)
    pasta_notebooks = os.path.dirname(os.path.abspath(__file__))
    raiz_projeto = os.path.dirname(pasta_notebooks)
    
    # Definir caminhos absolutos baseados na raiz
    caminho_raw = os.path.join(raiz_projeto, "data", "raw", "dados_brutos_frotas.csv")
    pasta_bronze = os.path.join(raiz_projeto, "data", "bronze")
    caminho_saida = os.path.join(pasta_bronze, "frotas_bronze.parquet")
    
    # Garantir que a pasta de destino exista
    os.makedirs(pasta_bronze, exist_ok=True)
    
    # Leitura dos dados brutos
    if not os.path.exists(caminho_raw):
        raise FileNotFoundError(f"❌ Arquivo não encontrado: {caminho_raw}")
        
    df_raw = pd.read_csv(caminho_raw)
    print(f"📦 Registros lidos da origem: {len(df_raw)}")
    
    # Adição de Metadados de Governança e Linhagem (Data Lineage)
    df_bronze = df_raw.copy()
    df_bronze['_data_ingestao'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_bronze['_arquivo_origem'] = os.path.basename(caminho_raw)
    
    # Escrita na Camada Bronze (Formato Parquet)
    df_bronze.to_parquet(caminho_saida, index=False)
    print(f"✅ Camada Bronze salva com sucesso em: {caminho_saida}")
    print(f"📊 Colunas na Bronze: {list(df_bronze.columns)}\n")

if __name__ == "__main__":
    executar_ingestao_bronze()