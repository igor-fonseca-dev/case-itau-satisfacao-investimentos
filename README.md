# 📊 Case Técnico: Satisfação de Investimentos — Itaú Unibanco

Repositório desenvolvido para o processo seletivo de Estágio em Engenharia de Dados (Diretoria de Investimentos / Experiência do Cliente). O objetivo deste projeto foi unificar fontes de dados heterogêneas, tratar inconsistências do mundo real e responder a uma pergunta de negócio crítica sobre a queda de satisfação no último trimestre.

---

## 🛠️ Justificativa Tecnológica (Por que Python e Pandas?)
Para este desafio, optei por utilizar **Python com a biblioteca Pandas**. 
* **Justificativa:** Como os dados de origem estavam em múltiplos formatos desconectados (um arquivo CSV digital, uma planilha Excel de atendimento manual e um extrato de sistema em CSV), o Python oferece uma versatilidade incomparável para o processo de *ETL (Extract, Transform, Load)* local. 
* O Pandas permitiu realizar a exploração rápida de colunas, criar tratamentos de valores nulos, estruturar funções iterativas de conversão de datas e aplicar mapeamentos de dicionários (*de-para*) de forma muito mais ágil e legível do que se exigisse a subida prévia para um banco de dados relacional via SQL.

---

## 📂 Estrutura do Repositório

```text
case-itau-satisfacao-investimentos/
│
├── data/
│   ├── raw/                        # Dados brutos originais (Formulário, Atendimento, Extrato)
│   └── clean/                      # Base consolidada gerada pelo pipeline (base_consolidada.csv)
│
├── src/
│   ├── checar_dados.py             # Script exploratório inicial (profiling de qualidade)
│   ├── unificar_e_tratar_dados.py  # Pipeline principal de engenharia (ETL)
│   └── analisando_negocio.py       # Script analítico focado na resposta de negócio (trimestres/motivos)
│
├── DECISOES.md                     # Documentação das premissas e escolhas de engenharia
├── ENTREGA_FINAL.md                # Entrega executiva, relato de IA e gestão de tempo
├── requirements.txt                # Dependências do projeto (pandas, openpyxl, etc.)
└── README.md                       # Visão geral do projeto

🛠️ Como Executar o Projeto
Se você quiser rodar este pipeline na sua máquina, siga os passos abaixo:

1 - Clone o repositório:

Bash
git clone [https://github.com/SEU-USUARIO/case-itau-satisfacao-investimentos.git](https://github.com/SEU-USUARIO/case-itau-satisfacao-investimentos.git)
cd case-itau-satisfacao-investimentos

2 -Crie e ative um ambiente virtual (Opcional, mas recomendado):

Bash
python -m venv venv
# No Windows (PowerShell):
.\venv\Scripts\Activate
# No Mac/Linux:
source venv/bin/activate

3 -Instale as dependências:

Bash
pip install -r requirements.txt

4 -Execute o pipeline de tratamento e unificação:

Bash
python src/unificar_e_tratar_dados.py
(O script irá ler as fontes brutas, tratar anomalias de notas e datas, unificar as chaves e salvar a base tratada em data/clean/base_consolidada.csv)

5 -Execute a análise de negócio:

Bash
python src/analisando_negocio.py
(Exibe no terminal a quebra por trimestres e os principais motivos de insatisfação dos clientes).

💡 Critérios e Decisões Tomadas Diante dos Dados Sujos
Diante das ambiguidades e imperfeições encontradas nas fontes originais, tomei as seguintes decisões de engenharia:

Reconciliação de IDs: O formulário digital trazia um prefixo textual (C00103), enquanto as outras bases usavam apenas números. Implementei uma extração via Expressões Regulares (regex) para isolar os dígitos e gerar uma chave primária numérica comum (id_cliente_num), viabilizando um merge externo (outer) sem perda de registros.

Tratamento de Anomalias de Notas: O atendimento manual continha notas por extenso ('dez') e valores fora da escala padrão (ex: '11'). O texto foi convertido numericamente para 10, e valores inválidos foram descartados (None) para não distorcer o cálculo da média, mantendo a linha do cliente para fins de contagem de volumetria.

Padronização Categórica: Nomes de produtos preenchidos manualmente apresentavam diversas variações e erros de digitação (ex: c.d.b., carteira adm). Criei um dicionário de mapeamento (de-para) explícito para consolidá-los nas 5 categorias oficiais do extrato.

## 🤖 Como Usei Inteligência Artificial no Projeto

* **Dinâmica de Desenvolvimento (*Pair Programming*):** Eu fui escrevendo o código do zero e estruturando a lógica principal. Conforme ia avançando, usava a IA como um suporte técnico rápido para otimizar trechos repetitivos, resolver bugs pontuais de sintaxe e refinar rotinas específicas (como o tratamento de múltiplos formatos de data).
* **Direção e Critério Meu:** A condução do projeto inteira veio da minha cabeça. Fui eu quem defini a regra de negócio, criei a hipótese analítica para entender a queda trimestral, filtrei os detratores e decidi como tratar cada sujeira encontrada nos dados. A IA só me ajudou a acelerar a digitação e a depurar mais rápido.

---

## ⏱️ Gestão de Tempo e Próximos Passos (Limitações)

* **Como dividi minhas ~5 horas de trabalho:**
  * **40% do tempo:** Olhando os dados brutos, entendendo a bagunça que estava nas planilhas e mapeando o que precisava ser limpo.
  * **40% do tempo:** Codando o pipeline de unificação (ETL) em Python para juntar tudo sem perder informação.
  * **20% do tempo:** Analisando os números no terminal, tirando os *insights* de negócio e estruturando a entrega.
**O que dá para melhorar (Limitação Atual):** Pra resolver rápido e focar no problema principal, fiz a normalização dos nomes de produtos usando um dicionário estático (*hardcoded*). Se fosse um ambiente de Big Data rodando em produção no banco com milhares de variações, o ideal seria implementar algum algoritmo de similaridade de texto (*Fuzzy Matching*) para automatizar essa limpeza.