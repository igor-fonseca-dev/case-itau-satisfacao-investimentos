import pandas as pd
import numpy as np

df = pd.read_csv('data/clean/base_consolidada.csv')

print("=== INVESTIGAÇÃO: QUEDA DE SATISFAÇÃO NO ÚLTIMO TRIMESTRE ===\n")

df['nota_final'] = pd.to_numeric(
    df['nota_satisfacao'],
    errors='coerce'
)

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

if 'principal_motivo_contato' in df.columns:
    print("\n2. Principais motivos de contato de quem deu nota baixa (<= 6):")
    motivos = notas_ruins['principal_motivo_contato'].value_counts().head(5)
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

print("\n4. Satisfação por produto no último trimestre:")

ultimo_trimestre = df[
    df['trimestre_ref'] == df['trimestre_ref'].max()
]

produto_ultimo_tri = (
    ultimo_trimestre
    .groupby('produto')
    .agg(
        nota_media=('nota_final', 'mean'),
        volume=('nota_final', 'count')
    )
    .sort_values('nota_media')
)

print(produto_ultimo_tri.to_string())
print("-" * 50)
print("\n5. Relação entre produto e tempo de resolução no último trimestre:")

produto_tempo = (
    ultimo_trimestre
    .groupby('produto')
    .agg(
        nota_media=('nota_final', 'mean'),
        tempo_medio_resolucao=('tempo_resolucao_horas', 'mean'),
        volume=('nota_final', 'count')
    )
    .sort_values('nota_media')
)

print(produto_tempo.to_string())
print("-" * 50)
print("\n6. Evolução da satisfação por produto:")

produto_trimestre = (
    df
    .groupby(['trimestre_ref', 'produto'])
    .agg(
        nota_media=('nota_final', 'mean'),
        volume=('nota_final', 'count')
    )
    .reset_index()
    .sort_values(['trimestre_ref', 'nota_media'])
)

print(produto_trimestre.to_string(index=False))
print("-" * 50)