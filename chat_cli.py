from app.agent import ask_agent

def main():
    print("=== Assistente de Auditoria (RAG + memória) ===")
    print("Escreve 'sair' para terminar.\n")

    session_id = "sessao-teste"

    while True:
        pergunta = input("Pergunta: ")
        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("Até logo!")
            break

        try:
            resposta = ask_agent(session_id, pergunta)
            print("\nResposta:\n", resposta)
            print("-" * 50)
        except Exception as e:
            print("Erro:", e)
            break

if __name__ == "__main__":
    main()
