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

formulario['id_cliente_num'] = formulario['id_cliente'].str.extract(r'(\d+)').astype(int)
atendimento['id_cliente_num'] = atendimento['codigo_cliente'].astype(str).str.strip().astype(int)
extrato['id_cliente_num'] = extrato['customer_id'].astype(int)

def normalizar_nota(valor):
    if pd.isna(valor):
        return None
    texto = str(valor).strip().lower()
    if texto == 'dez':
        return 10.0
    try:
        nota = float(texto)
        return nota if 0 <= nota <= 10 else None
    except ValueError:
            return None

    atendimento ['nota_limpa'] = atendimento['nota'].apply(normalizar_nota)

    formatos_data = ['%Y-%m-%d', '%d/%m/%Y', '%d-%b-%y']

def normalizar_data(valor):
    if pd.isna(valor):
        return pd.NaT
    for fmt in formatos_data:
        try:
            return pd.to_datetime(str(valor).strip(), format=fmt)
        except ValueError:
                continue
    return pd.NaT

    atendimento['data_limpa'] = atendimento['data'].apply(normalizar_data)

mapa_atendimento = {
    'cdb': 'CDB', 'c.d.b.': 'CDB',
    'coe': 'COE', 'c.o.e.': 'COE',
    'carteira adm': 'Carteira Administrada', 'carteira administrada': 'Carteira Administrada',
    'fundo': 'Fundos', 'fundos': 'Fundos', 'fundos de investimento': 'Fundos',
    'tesouro': 'Tesouro Direto', 'tesouro direto': 'Tesouro Direto'
}
atendimento['produto_limpo'] = atendimento['produto_investimento'].str.strip().str.lower().map(mapa_atendimento)

mapa_extrato = {
    'PRD_CDB': 'CDB', 'PRD_COE': 'COE', 'PRD_CAR': 'Carteira Administrada',
    'PRD_FND': 'Fundos', 'PRD_TES': 'Tesouro Direto'
}
extrato['produto_limpo'] = extrato['produto_codigo'].map(mapa_extrato)

df_final = extrato.merge(formulario, on='id_cliente_num', how='outer', suffixes=('_extrato', '_form'))
df_final = df_final.merge(atendimento, on='id_cliente_num', how='outer')

os.makedirs('data/clean', exist_ok=True)
df_final.to_csv('data/clean/base_consolidada.csv', index=False)
    
print("=== PIPELINE CONCLUÍDO ===")
print(f"Total de registros na base consolidada: {len(df_final)}")
print("Arquivo salvo em: data/clean/base_consolidada.csv")