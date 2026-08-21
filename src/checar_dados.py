import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 150)

formulario = pd.read_csv('data/raw/formulario_digital.csv')
atendimento = pd.read_excel('data/raw/atendimento_manual.xlsx')
extrato = pd.read_csv('data/raw/extrato_sistema.csv')

for nome, df in [('formulario_digital', formulario), ('atendimento_manual', atendimento), ('extrato_sistema', extrato)]:
    print(f"\n{'='*60}\n{nome}\n{'='*60}")
    print(f"Linhas: {len(df)}, Colunas: {list(df.columns)}")
    print("\nTipos de dado:")
    print(df.dtypes)
    print('\nValores nulos por coluna:')
    print(df.isnull().sum())
    print('\nAmostra (5 primeiras linhas):')
    print(df.head())
    print('\n\n=== INVESTIGAÇÃO DE DADOS: coluna "nota" do atendimento(valores únicos) ===')
    print(sorted(atendimento['nota'].dropna().unique(), key=str))

    print ('\n=== INVESTIGAÇÃO DE DADOS: formatos de data em atendimento_manual (amostra) ===')
    print(atendimento['data'].unique()[:20])

    print ('\n=== INVESTIGAÇÃO DE DADOS: nomes de produto em cada fonte ===')
    print("formulario:", sorted(formulario['produto'].unique()))
    print("atendimento:", sorted(atendimento['produto_investimento'].unique()))
    print("extrato:", sorted(extrato['produto_codigo'].unique()))