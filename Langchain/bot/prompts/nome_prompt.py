from google.ai import generativelanguage as gl
from google.api_core.client_options import ClientOptions
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("Faltando GOOGLE_API_KEY no .env")

client_options = ClientOptions(api_key=API_KEY)
client = gl.TextServiceClient(client_options=client_options)

SYSTEM_PROMPT = """
Você é um assistente virtual que coleta dados de clientes para planos de saúde.
Siga esta ordem:
1. Nome completo (peça sobrenome se só nome)
2. Idade
3. CPF
4. Endereço (pergunte complemento)
5. Email
6. Filhos? (verdadeiro/falso)
7. Idade dos filhos (valide que sejam menores que cliente)
8. Plano desejado (ofereça só os que temos)

Pergunte um dado por vez, seja educado e confirme dados quando necessário.
"""

historico = [SYSTEM_PROMPT]

def enviar_mensagem_usuario(texto_usuario: str) -> str:
    global historico
    historico.append(f"Usuário: {texto_usuario}")

    prompt_texto = "\n".join(historico) + "\nAssistente:"

    response = client.generate_text(
        model="models/text-bison-001",
        prompt=gl.TextPrompt(text=prompt_texto),
        temperature=0.3,
        top_p=0.95,
        top_k=40,
        candidate_count=1
    )
    resposta = response.candidates[0].output.strip()
    historico.append(f"Assistente: {resposta}")

    return resposta


if __name__ == "__main__":
    print("Assistente Virtual - Gemini API (modo texto concatenado)")

    while True:
        user_input = input("Você: ").strip()
        if user_input.lower() in ["sair", "exit", "quit"]:
            print("Encerrando o atendimento. Até logo!")
            break

        resposta = enviar_mensagem_usuario(user_input)
        print("Bot:", resposta)
