'''

PAPEL:
Atue como um CEO visionário do setor de tecnologia limpa, acostumado a elaborar 
posicionamentos estratégicos para investidores e stakeholders.

TAREFA:
Redija um ensaio que responda às seguintes questões:

Principais tendências de descarbonização para os próximos 5 anos.

Oportunidades de mercado para startups de captura de carbono.

Riscos regulatórios globais a curto, médio e longo prazo.
Inclua exemplos reais, dados de mercado de pelo menos 3 relatórios (cite fonte e ano) 
e conclua com um call-to-action para potenciais parceiros.

FORMATO:
Forneça o ensaio em forma de lista hierárquica com, no mínimo, três níveis de indentação 
(tópico, subtópico e bullet).


'''

# import libs
from langchain import output_parsers
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, prompt
from dotenv import load_dotenv

from langchain.output_parsers import ResponseSchema, StructuredOutputParser


load_dotenv()


# Prompt

schema_papel = ResponseSchema(
    name='Papel',
    type='str',
    description='Atue como um CEO visionário do setor de tecnologia limpa, acostumado a elaborar'\
    'posicionamentos estratégicos para investidores e stakeholders.'
)

schema_tarefa = ResponseSchema(
    name='Tarefa',
    type='str',
    description='Redija um ensaio que responda às seguintes questões:'\
    'Principais tendências de descarbonização para os próximos 5 anos.'\
    'Oportunidades de mercado para startups de captura de carbono.'\
    'Riscos regulatórios globais a curto, médio e longo prazo.'
)

schema_Dados_Mercado = ResponseSchema(
    name='Dados_Mercado',
    type='list',
    description=' Inclua exemplos reais, dados de mercado de pelo menos 3 relatórios (cite fonte e ano)'

)

schema_call_to_action = ResponseSchema(
    name='call-to-action',
    type='str',
    description='e conclua com um call-to-action para potenciais parceiros.'
)

schema_Formato = ResponseSchema(
    name='Formato',
    type='str',
    description='Forneça o ensaio em forma de lista hierárquica com, no mínimo, três níveis de'\
        'indentação (tópico, subtópico e bullet).'
)

response_schema = [
    schema_papel,
    schema_tarefa,
    schema_Dados_Mercado,
    schema_call_to_action,
    schema_Formato
]

output_parsers = StructuredOutputParser.from_response_schemas(response_schema)

schema_formatado = output_parsers.get_format_instructions()

prompt_template = ChatPromptTemplate.from_template(
    '''
    Você é um CEO visionário do setor de tecnologia limpa. Responda as seguintes perguntas de forma clara e estruturada:

1. Principais tendências de descarbonização para os próximos 5 anos.
2. Oportunidades de mercado para startups de captura de carbono.
3. Riscos regulatórios globais a curto, médio e longo prazo.

Use o formato JSON conforme o esquema:

{Instrucoes}
    '''
)

llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash')

resposta = llm.invoke(prompt_template.format_messages(Instrucoes= response_schema))


print(resposta.content)