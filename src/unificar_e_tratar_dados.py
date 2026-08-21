import pandas as pd
import os
import sys

print("Executando pipeline de unificação e tratamento de dados...\n")

try:
    formulario = pd.read_csv('data/raw/formulario_digital.csv')
    atendimento = pd.read_excel('data/raw/atendimento_manual.xlsx')
    extrato = pd.read_csv('data/raw/extrato_sistema.csv')

except FileNotFoundError as e:
    print(f"Erro ao ler os arquivos: {e}")
    sys.exit()

formulario['id_cliente_num'] = (
    formulario['id_cliente']
    .astype(str)
    .str.extract(r'(\d+)')[0]
    .astype(int)
)

atendimento['id_cliente_num'] = (
    atendimento['codigo_cliente']
    .astype(str)
    .str.strip()
    .astype(int)
)

extrato['id_cliente_num'] = (
    extrato['customer_id']
    .astype(int)
)

def normalizar_nota(valor):
    if pd.isna(valor):
        return None

    texto = str(valor).strip().lower()

    if texto == 'dez':
        return 10.0

    try:
        nota = float(texto)

        if 0 <= nota <= 10:
            return nota

        return None

    except ValueError:
        return None

atendimento['nota_limpa'] = atendimento['nota'].apply(normalizar_nota)

formatos_data = [
    '%Y-%m-%d',
    '%d/%m/%Y',
    '%d-%b-%y'
]

def normalizar_data(valor):
    if pd.isna(valor):
        return pd.NaT

    for fmt in formatos_data:
        try:
            return pd.to_datetime(
                str(valor).strip(),
                format=fmt
            )

        except ValueError:
            continue

    return pd.NaT

atendimento['data_limpa'] = atendimento['data'].apply(normalizar_data)

mapa_atendimento = {
    'cdb': 'CDB',
    'c.d.b.': 'CDB',

    'coe': 'COE',
    'c.o.e.': 'COE',

    'carteira adm': 'Carteira Administrada',
    'carteira administrada': 'Carteira Administrada',

    'fundo': 'Fundos',
    'fundos': 'Fundos',
    'fundos de investimento': 'Fundos',

    'tesouro': 'Tesouro Direto',
    'tesouro direto': 'Tesouro Direto'
}


atendimento['produto_limpo'] = (
    atendimento['produto_investimento']
    .astype(str)
    .str.strip()
    .str.lower()
    .map(mapa_atendimento)
)

mapa_extrato = {
    'PRD_CDB': 'CDB',
    'PRD_COE': 'COE',
    'PRD_CAR': 'Carteira Administrada',
    'PRD_FND': 'Fundos',
    'PRD_TES': 'Tesouro Direto'
}


extrato['produto_limpo'] = (
    extrato['produto_codigo']
    .map(mapa_extrato)
)

atendimento_agg = (
    atendimento
    .groupby('id_cliente_num')
    .agg(
        qtd_atendimentos=(
            'id_cliente_num',
            'size'
        ),

        nota_atendimento_media=(
            'nota_limpa',
            'mean'
        ),

        qtd_atendimentos_resolvidos=(
            'status_resolucao',
            lambda x: (
                x.astype(str)
                .str.strip()
                .str.lower()
                == 'resolvido'
            ).sum()
        ),

        qtd_atendimentos_pendentes=(
            'status_resolucao',
            lambda x: (
                x.astype(str)
                .str.strip()
                .str.lower()
                == 'pendente'
            ).sum()
        ),

        principal_motivo_contato=(
            'motivo_contato',
            lambda x: (
                x.dropna().mode().iloc[0]
                if not x.dropna().empty
                else None
            )
        ),

        principal_canal_atendimento=(
            'canal_atendimento',
            lambda x: (
                x.dropna().mode().iloc[0]
                if not x.dropna().empty
                else None
            )
        ),

        produto_atendimento=(
            'produto_limpo',
            lambda x: (
                x.dropna().mode().iloc[0]
                if not x.dropna().empty
                else None
            )
        )
    )
    .reset_index()
)

extrato_agg = (
    extrato
    .groupby('id_cliente_num')
    .agg(
        qtd_registros_extrato=(
            'id_cliente_num',
            'size'
        ),

        qtd_acessos_app_30d=(
            'qtd_acessos_app_30d',
            'mean'
        ),

        qtd_reclamacoes_90d=(
            'qtd_reclamacoes_90d',
            'mean'
        ),

        tempo_resolucao_horas=(
            'tempo_resolucao_horas',
            'mean'
        ),

        suitability_pendente=(
            'suitability_pendente',
            'max'
        ),

        produto_extrato=(
            'produto_limpo',
            lambda x: (
                x.dropna().mode().iloc[0]
                if not x.dropna().empty
                else None
            )
        )
    )
    .reset_index()
)

df_final = formulario.merge(
    atendimento_agg,
    on='id_cliente_num',
    how='left'
)

df_final = df_final.merge(
    extrato_agg,
    on='id_cliente_num',
    how='left'
)

os.makedirs(
    'data/clean',
    exist_ok=True
)

df_final.to_csv(
    'data/clean/base_consolidada.csv',
    index=False
)

print("=== PIPELINE CONCLUÍDO ===")
print(f"Total de registros na base consolidada: {len(df_final)}")
print(f"Clientes únicos na base consolidada: {df_final['id_cliente_num'].nunique()}")
print(f"Pesquisas no formulário original: {len(formulario)}")
print("Arquivo salvo em: data/clean/base_consolidada.csv")