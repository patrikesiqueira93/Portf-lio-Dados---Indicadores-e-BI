import os
import pandas as pd

def executar_agregacao_gold():
    print("🚀 Iniciando criação da Camada Gold (Star Schema)...")
    
    # 1. Localizar caminhos baseados na raiz do projeto
    pasta_notebooks = os.path.dirname(os.path.abspath(__file__))
    raiz_projeto = os.path.dirname(pasta_notebooks)
    
    caminho_silver = os.path.join(raiz_projeto, "data", "silver", "frotas_silver.parquet")
    pasta_gold = os.path.join(raiz_projeto, "data", "gold")
    os.makedirs(pasta_gold, exist_ok=True)
    
    # 2. Leitura da Camada Silver
    if not os.path.exists(caminho_silver):
        raise FileNotFoundError(f"❌ Arquivo Silver não encontrado: {caminho_silver}")
        
    df_silver = pd.read_parquet(caminho_silver)
    
    # -------------------------------------------------------------
    # 3. Criar Dimensão Equipamento (dim_equipamento)
    # -------------------------------------------------------------
    dim_equipamento = df_silver[['id_ativo', 'categoria_equipamento', 'filial_operacao']].drop_duplicates().reset_index(drop=True)
    dim_equipamento['sk_equipamento'] = dim_equipamento.index + 1
    
    # -------------------------------------------------------------
    # 4. Criar Dimensão Tempo (dim_tempo)
    # -------------------------------------------------------------
    datas = pd.date_range(start=df_silver['dt_abertura_chamado'].min(), end=df_silver['dt_abertura_chamado'].max(), freq='D')
    dim_tempo = pd.DataFrame({'data': datas})
    dim_tempo['sk_tempo'] = dim_tempo['data'].dt.strftime('%Y%m%d').astype(int)
    dim_tempo['ano'] = dim_tempo['data'].dt.year
    dim_tempo['mes'] = dim_tempo['data'].dt.month
    dim_tempo['nome_mes'] = dim_tempo['data'].dt.strftime('%B')
    dim_tempo['trimestre'] = dim_tempo['data'].dt.quarter
    dim_tempo['dia_semana'] = dim_tempo['data'].dt.strftime('%A')
    
    # -------------------------------------------------------------
    # 5. Criar Tabela Fato (fato_chamados)
    # -------------------------------------------------------------
    df_fato = df_silver.merge(dim_equipamento, on=['id_ativo', 'categoria_equipamento', 'filial_operacao'], how='left')
    df_fato['sk_tempo'] = pd.to_datetime(df_fato['dt_abertura_chamado']).dt.strftime('%Y%m%d').astype(int)
    
    fato_chamados = df_fato[[
        'id_chamado',
        'sk_equipamento',
        'sk_tempo',
        'dt_abertura_chamado',
        'dt_conclusao_chamado',
        'sla_prometido_horas',
        'tempo_atendimento_horas',
        'custo_manutencao',
        'fl_estourou_sla',
        'horas_atraso',
        'status_ativo'
    ]]
    
    # -------------------------------------------------------------
    # 6. Salvar Tabelas da Camada Gold em Parquet
    # -------------------------------------------------------------
    dim_equipamento.to_parquet(os.path.join(pasta_gold, "dim_equipamento.parquet"), index=False)
    dim_tempo.to_parquet(os.path.join(pasta_gold, "dim_tempo.parquet"), index=False)
    fato_chamados.to_parquet(os.path.join(pasta_gold, "fato_chamados.parquet"), index=False)
    
    print("✅ Camada Gold gerada com sucesso!")
    print(f"   • dim_equipamento: {len(dim_equipamento)} registros")
    print(f"   • dim_tempo: {len(dim_tempo)} dias registrados")
    print(f"   • fato_chamados: {len(fato_chamados)} registros\n")

if __name__ == "__main__":
    executar_agregacao_gold()