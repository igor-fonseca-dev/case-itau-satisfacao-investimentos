import pandas as pd
import numpy as np

df = pd.read_csv('data/clean/base_consolidada.csv')

print("=== INVESTIGAÇÃO: QUEDA DE SATISFAÇÃO NO ÚLTIMO TRIMESTRE ===\n")

df['nota_manual_num'] = pd.to_numeric(df['nota'].replace('dez', 10, regex=True), errors='coerce')

df['nota_final'] = df['nota_satisfacao'].fillna(df['nota_manual_num'])

if 'trimestre_ref' in df.columns:
    print("1. Como as notas se comportaram ao longo dos trimestres?")
    
    evolucao = df.groupby('trimestre_ref').agg(
        qtde_avaliacoes=('nota_final', 'count'),
        nota_media=('nota_final', 'mean')
    ).reset_index()
    
    evolucao = evolucao.sort_values('trimestre_ref')
    print(evolucao.to_string(index=False))
    print("-" * 50)

notas_ruins = df[df['nota_final'] <= 6]

if 'motivo_contato' in df.columns:
    print("\n2. Principais motivos de contato de quem deu nota baixa (<= 6):")
    motivos = notas_ruins['motivo_contato'].value_counts().head(5)
    print(motivos)
    print("-" * 50)

if 'tempo_resolucao_horas' in df.columns:
    print("\n3. Será que a demora no atendimento derrubou a nota?")
    
    df['faixa_de_demora'] = pd.qcut(df['tempo_resolucao_horas'], q=3, labels=['Rápido', 'Médio', 'Demorado'])
    
    impacto_demora = df.groupby('faixa_de_demora').agg(
        nota_media=('nota_final', 'mean'),
        volume=('nota_final', 'count')
    )
    print(impacto_demora)