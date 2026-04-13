import os

def cortar(data, holerite_path, ponto_path):
    # Cria a pasta de resultados na raiz
    nome_da_pasta = "RESULTADOS_TESTE"
    if not os.path.exists(nome_da_pasta):
        os.makedirs(nome_da_pasta)

    # Cria um arquivo de log simples
    caminho_log = os.path.join(nome_da_pasta, "log_execucao.txt")
    with open(caminho_log, "a", encoding="utf-8") as f:
        f.write(f"Executado para data: {data}\n")
    
    print(f"--- SCRIPT EXECUTADO COM SUCESSO PARA A DATA {data} ---")
    return True