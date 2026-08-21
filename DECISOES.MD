# Registro de Decisões: Tratamento e Limpeza de Dados

Durante a etapa de exploração dos dados brutos (via script de profilaxia `checar_dados.py`), identifiquei algumas inconsistências esperadas ao lidar com fontes distintas (formulário, atendimento manual e extrato). 

Abaixo, registro como decidi tratar cada anomalia para garantir a integridade da base unificada:

### 1. Chave de Cliente (ID)
- **O Cenário:** O `formulario_digital` traz um prefixo "C" (ex: C00103), enquanto o `atendimento_manual` e o `extrato_sistema` trazem apenas números (int).
- **A Decisão:** Para conseguir cruzar (fazer o *merge*) das três bases, decidi extrair apenas os dígitos do formulário e criar uma coluna padrão `id_cliente_num` (inteiro) em todas as tabelas. Essa será nossa chave primária.

### 2. Tratamento das Notas de Satisfação
- **O Cenário:** A coluna `nota` no atendimento manual deveria ir de 0 a 10, mas encontrei valores como `'dez'` (texto) e `'11'` (fora da escala).
- **A Decisão:** 
  - Converti `'dez'` para o número `10`, pois a intenção do cliente é clara. 
  - Registros com nota `'11'` foram transformados em nulos (NaN) para não enviesar a média de satisfação, mas a linha do cliente foi mantida para não perdermos o volume de atendimentos daquele produto.

### 3. Inconsistência nas Datas
- **O Cenário:** A inserção manual gerou formatos variados (ex: `2026-03-01`, `02/03/2026`, `10-Mar-26`).
- **A Decisão:** Criei uma função que tenta converter a string iterando por uma lista de formatos conhecidos. O que não der "match" vira nulo (NaT - Not a Time), permitindo analisar a sujeira sem quebrar o pipeline.

### 4. Padronização de Produtos
- **O Cenário:** O extrato traz códigos como `PRD_CDB`, e o atendimento traz texto livre com erros de digitação (ex: `c.o.e.`, `cdb`).
- **A Decisão:** Fiz um mapeamento (*de-para*) forçando os nomes para as 5 categorias oficiais encontradas no formulário (CDB, COE, Carteira Administrada, Fundos, Tesouro Direto). Para garantir, passei tudo do atendimento para minúsculo antes de mapear.