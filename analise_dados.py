import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

print("1. Conectando ao Banco de Dados PostgreSQL...")
engine = create_engine('postgresql://postgres:159357@localhost:5432/postgres')

print("2. Extraindo a base de clientes...")
df = pd.read_sql('SELECT * FROM analytics.clientes_credito', engine)

print("3. Processando Regras de Negócio (Motor de Risco)...")
# Função que simula uma regra de negócio de um banco
def classificar_risco(renda):
    if renda < 3000:
        return 'Alto Risco'
    elif renda < 8000:
        return 'Médio Risco'
    else:
        return 'Baixo Risco'

# Aplica a regra criando uma nova coluna no DataFrame
df['perfil_risco'] = df['renda_mensal'].apply(classificar_risco)

print("4. Agregando os dados para a Diretoria...")
# Agrupa os dados pelo perfil de risco e calcula métricas
resumo = df.groupby('perfil_risco')['renda_mensal'].agg(['count', 'mean', 'min', 'max']).round(2)
resumo.columns = ['Total Clientes', 'Renda Média', 'Renda Mínima', 'Renda Máxima']

print("5. Gerando os Relatórios Automatizados...")
data_hora_atual = datetime.now().strftime('%Y-%m-%d_%H-%M')

# Exportação 1: Planilha CSV para a equipe de analistas
arquivo_csv = f'base_segmentada_{data_hora_atual}.csv'
resumo.to_csv(arquivo_csv)

# Exportação 2: Sumário Executivo em Texto para a gestão
arquivo_txt = f'sumario_executivo_{data_hora_atual}.txt'
with open(arquivo_txt, 'w', encoding='utf-8') as f:
    f.write("="*60 + "\n")
    f.write(f"  SUMÁRIO EXECUTIVO DE RISCO DE CRÉDITO - {data_hora_atual}\n")
    f.write("="*60 + "\n\n")
    f.write(f"-> Total de Clientes Analisados da Carteira: {len(df)}\n")
    f.write(f"-> Renda Média Geral da Carteira: R$ {df['renda_mensal'].mean():.2f}\n\n")
    f.write("DISTRIBUIÇÃO POR PERFIL DE RISCO:\n")
    f.write("-" * 60 + "\n")
    f.write(resumo.to_string())
    f.write("\n\n" + "="*60 + "\n")
    f.write("Relatório gerado automaticamente pelo Pipeline de Dados.\n")

print(f"Sucesso Total! Arquivos gerados na pasta do projeto:\n - {arquivo_csv}\n - {arquivo_txt}")