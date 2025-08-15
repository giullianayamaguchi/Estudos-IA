'''
PAPEL:
Atue como um Analista de Dados Sênior, especializado em processar informações não estruturadas (como notícias) e transformá-las em insights acionáveis para uma empresa de investimentos.

TAREFA:
Processe o artigo de notícias financeiras fictício abaixo e extraia as seguintes informações-chave:

Nome da empresa principal.

O ticker (símbolo na bolsa) da ação da empresa.

O nome do novo produto lançado.

Uma lista com os nomes dos concorrentes mencionados.

O valor numérico da previsão de mercado (em milhões).

O sentimento geral do artigo (Positivo, Neutro ou Negativo).

Texto para Análise:

A gigante de tecnologia InovaTech (ticker: INVT) anunciou hoje o lançamento de sua 
nova plataforma de inteligência artificial, a "QuantumLeap AI", prometendo revolucionar o mercado. 
Analistas preveem que a plataforma pode capturar um mercado de até 500 milhões de dólares no 
primeiro ano. A notícia chega para acirrar a competição com sua principal rival, a OmniCorp, 
que viu suas ações caírem 2% após o anúncio. O clima geral é de grande otimismo para o futuro 
da InovaTech.
FORMATO:
Forneça a saída estritamente como um objeto JSON.
'''


# texto

texto_base = 'A gigante de tecnologia InovaTech (ticker: INVT) anunciou hoje o lançamento de sua' \
'nova plataforma de inteligência artificial, a "QuantumLeap AI", prometendo revolucionar o mercado. ' \
'Analistas preveem que a plataforma pode capturar um mercado de até 500 milhões de dólares no ' \
'primeiro ano. A notícia chega para acirrar a competição com sua principal rival, a OmniCorp, ' \
'que viu suas ações caírem 2% após o anúncio. O clima geral é de grande otimismo para o futuro ' \
'da InovaTech.' \

#importandao libs

from token import TYPE_COMMENT
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain import output_parsers
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from dotenv import load_dotenv

# carregar arq .env

load_dotenv()

#Schemas 

schema_nome = ResponseSchema(
    name='Nome',
    type='str',
    description='Nome da empresa principal.'
)

schema_ticker = ResponseSchema(

    name='ticker',
    type='str',
    description='O ticker (símbolo na bolsa) da ação da empresa.'
)

schema_produto = ResponseSchema(
    name='novo_produto',
    type='str',
    description='O nome do novo produto lançado.'
)

schema_concorrentes = ResponseSchema(
    name='Concorrentes',
    type='list',
    description='Uma lista com os nomes dos concorrentes mencionados.'
)

schema_previsao_mercado =ResponseSchema(
    name='previsao_mercado',
    type='float',
    description='O valor numérico da previsão de mercado (em milhões), caso sja necessário utilizar a vírgula, use só 2 casas'
)

schema_sentimento = ResponseSchema(
    name='Sentimento_geral',
    type='str',
    description='O sentimento geral do artigo (Positivo, Neutro ou Negativo).'
)

respose_schema = [
    schema_nome,
    schema_ticker,
    schema_produto,
    schema_concorrentes,
    schema_previsao_mercado,
    schema_sentimento
]

output_parsers = StructuredOutputParser.from_response_schemas(respose_schema)

schema_formatado = output_parsers.get_format_instructions()

# prompt 

prompt_template = ChatPromptTemplate.from_template(
    '''
    Atue como um Analista de Dados Sênior, especializado em processar informações 
    não estruturadas (como notícias) e transformá-las em insights acionáveis para uma 
    empresa de investimentos.

    Processe o artigo de notícias financeiras fictício abaixo e extraia as seguintes 
    informações-chave retorne no formato json:

Nome da empresa principal.

O ticker (símbolo na bolsa) da ação da empresa.

O nome do novo produto lançado.

Uma lista com os nomes dos concorrentes mencionados.

O valor numérico da previsão de mercado (em milhões).

O sentimento geral do artigo (Positivo, Neutro ou Negativo).

"É crucial que os nomes das chaves no JSON de saída sejam **exatamente** os seguintes: 
nome_empresa, ticker_acao, nome_produto, concorrentes, previsao_mercado_milhoes, sentimento."
Texto = {texto}

    '''
)

llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash')

resposta = llm.invoke(prompt_template.format_messages(texto = texto_base))

print(resposta.content)