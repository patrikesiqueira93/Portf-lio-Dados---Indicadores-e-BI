import os
import pandas as pd

def executar_transformacao_silver():
    print("🚀 Iniciando transformação da Camada Silver...")
    
    # 1. Definir caminhos baseados na raiz do projeto
    pasta_notebooks = os.path.dirname(os.path.abspath(__file__))
    raiz_projeto = os.path.dirname(pasta_notebooks)
    
    caminho_bronze = os.path.join(raiz_projeto, "data", "bronze", "frotas_bronze.parquet")
    pasta_silver = os.path.join(raiz_projeto, "data", "silver")
    caminho_saida = os.path.join(pasta_silver, "frotas_silver.parquet")
    
    os.makedirs(pasta_silver, exist_ok=True)
    
    # 2. Leitura dos dados da Camada Bronze
    if not os.path.exists(caminho_bronze):
        raise FileNotFoundError(f"❌ Arquivo Bronze não encontrado: {caminho_bronze}")
        
    df_silver = pd.read_parquet(caminho_bronze)
    registros_iniciais = len(df_silver)
    print(f"📦 Registros lidos da Bronze: {registros_iniciais}")
    
    # 3. Limpeza & Deduplicação
    df_silver = df_silver.drop_duplicates(subset=['id_chamado']).copy()
    
    # 4. Conversão e Padronização de Tipos
    df_silver['dt_abertura_chamado'] = pd.to_datetime(df_silver['dt_abertura_chamado'])
    df_silver['custo_manutencao'] = df_silver['custo_manutencao'].astype(float).round(2)
    df_silver['tempo_atendimento_horas'] = df_silver['tempo_atendimento_horas'].astype(float).round(1)
    df_silver['sla_prometido_horas'] = df_silver['sla_prometido_horas'].astype(int)
    
    # 5. Aplicação de Regras de Negócio e KPIs de Eficiência
    # A) Calcular Data de Conclusão baseada no tempo de atendimento
    df_silver['dt_conclusao_chamado'] = df_silver['dt_abertura_chamado'] + pd.to_timedelta(df_silver['tempo_atendimento_horas'], unit='h')
    
    # B) Flag de Cumprimento de SLA (0 = Dentro do Prazo | 1 = Estourou SLA)
    df_silver['fl_estourou_sla'] = (df_silver['tempo_atendimento_horas'] > df_silver['sla_prometido_horas']).astype(int)
    
    # C) Calcular Horas de Atraso em Relação à Meta
    df_silver['horas_atraso'] = (df_silver['tempo_atendimento_horas'] - df_silver['sla_prometido_horas']).apply(lambda x: max(0, round(x, 1)))
    
    # 6. Escrita na Camada Silver (Formato Parquet)
    df_silver.to_parquet(caminho_saida, index=False)
    print(f"✅ Camada Silver salva com sucesso em: {caminho_saida}")
    print(f"📊 Resumo dos KPIs Calculados:")
    print(f"   • Total de Chamados: {len(df_silver)}")
    print(f"   • % Cumprimento de SLA: {((1 - df_silver['fl_estourou_sla'].mean()) * 100):.1f}%")
    print(f"   • Custo Total de Manutenção: R$ {df_silver['custo_manutencao'].sum():,.2f}\n")

if __name__ == "__main__":
    executar_transformacao_silver()