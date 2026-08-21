# Registro de Decisões: Tratamento e Limpeza de Dados

Durante a etapa de exploração dos dados brutos, realizada por meio do script de profilaxia `checar_dados.py`, foram identificadas inconsistências decorrentes das diferentes origens dos dados (formulário digital, atendimento manual e extrato do sistema).

Abaixo, estão documentadas as principais decisões tomadas durante o processo de tratamento e unificação das bases.

### 1. Chave de Cliente (ID)

- **O Cenário:** O `formulario_digital` utiliza um prefixo "C" (ex.: `C00103`), enquanto o `atendimento_manual` e o `extrato_sistema` utilizam apenas valores numéricos.

- **A Decisão:** Para permitir o cruzamento das três bases, foram extraídos apenas os dígitos do identificador presente no formulário. Em seguida, foi criada a coluna padronizada `id_cliente_num`, com tipo inteiro, utilizada como chave de integração entre as tabelas.

### 2. Tratamento das Notas de Satisfação

- **O Cenário:** A coluna `nota` do atendimento manual deveria apresentar valores entre 0 e 10, porém foram encontrados registros como `'dez'` (texto) e `'11'` (fora da escala).

- **A Decisão:**
  - O valor `'dez'` foi convertido para `10`, pois representa claramente uma nota válida.
  - O valor `'11'` foi convertido para nulo (`NaN`), evitando distorções no cálculo da média de satisfação.
  - O registro do cliente foi mantido para preservar o volume de atendimentos e permitir análises posteriores.

### 3. Inconsistência nas Datas

- **O Cenário:** A inserção manual resultou em diferentes formatos de data, como `2026-03-01`, `02/03/2026` e `10-Mar-26`.

- **A Decisão:** Foi criada uma função de conversão que tenta interpretar as datas utilizando uma lista de formatos conhecidos. Valores que não correspondem a nenhum formato válido são convertidos para `NaT` (*Not a Time*), permitindo preservar o registro sem interromper a execução do pipeline.

### 4. Padronização de Produtos

- **O Cenário:** O extrato utiliza códigos como `PRD_CDB`, enquanto o atendimento manual contém descrições em texto livre e possíveis variações ou erros de digitação, como `c.o.e.` e `cdb`.

- **A Decisão:** Foi criado um mapeamento (*de-para*) para padronizar os produtos de acordo com as cinco categorias oficiais identificadas no formulário:

  - CDB
  - COE
  - Carteira Administrada
  - Fundos
  - Tesouro Direto

  Antes do mapeamento, os valores provenientes do atendimento manual foram convertidos para letras minúsculas, reduzindo diferenças causadas por capitalização.

### 5. Limitações e Próximos Passos

Para manter o pipeline simples e resolver o problema dentro do escopo do projeto, a padronização dos nomes dos produtos foi realizada inicialmente utilizando um dicionário estático (*hardcoded*).

Em um ambiente de produção com maior volume e variedade de dados, seria recomendável substituir ou complementar essa abordagem por técnicas de similaridade de texto (*Fuzzy Matching*), permitindo identificar automaticamente variações e possíveis erros de digitação.

Essa abordagem também reduziria a necessidade de manutenção manual do dicionário à medida que novas variações de produtos fossem identificadas.
