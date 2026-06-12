import os
import subprocess

def listar_pastas_entrada():
    entrada = "ENTRADA"
    if not os.path.exists(entrada):
        print("❌ ERRO: Pasta ENTRADA não encontrada.")
        return []
    return [p for p in os.listdir(entrada) if os.path.isdir(os.path.join(entrada, p))]

def escolher_opcao(opcoes, mensagem):
    print(mensagem)
    for i, opcao in enumerate(opcoes, 1):
        print(f"{i}. {opcao}")
    escolha = input("Digite o número da opção desejada: ")
    try:
        idx = int(escolha) - 1
        if 0 <= idx < len(opcoes):
            return opcoes[idx]
    except ValueError:
        pass
    print("Opção inválida. Usando padrão:", opcoes[0])
    return opcoes[0]

def main():
    print("========================================")
    print("FILE ORGANIZER PIPELINE - MENU INTERATIVO")
    print("========================================\n")

    # Escolher pasta original
    pastas = listar_pastas_entrada()
    if not pastas:
        return
    pasta_escolhida = escolher_opcao(pastas, "Escolha a pasta desorganizada dentro de ENTRADA:")
    folder_original = os.path.join("ENTRADA", pasta_escolhida)

    # Escolher se move ou copia
    acao = escolher_opcao(["Copiar arquivos", "Mover arquivos"], "Deseja copiar ou mover os arquivos?")
    move_flag = "--move_files" if acao == "Mover arquivos" else "--copy_files"

    # Escolher tipo de relatório
    relatorio = escolher_opcao(["TXT", "JSON", "Ambos"], "Escolha o tipo de relatório:")
    if relatorio == "TXT":
        report_flags = "--txt"
    elif relatorio == "JSON":
        report_flags = "--json"
    else:
        report_flags = "--txt --json"

    # Escolher tipo de log
    log = escolher_opcao(["TXT", "JSON"], "Escolha o tipo de log:")
    log_flag = "--log_json" if log == "JSON" else "--log_txt"

    # Escolher se usa extension.json ou manual
    ext_choice = escolher_opcao(["Usar extension.json", "Definir manualmente"], "Deseja usar o extension.json ou definir manualmente?")
    if ext_choice == "Definir manualmente":
        print("Digite os mapeamentos no formato EXT:PASTA separados por espaço (ex: csv:csv txt:txt png:images pdf:docs)")
        ext_input = input("Mapeamentos: ").strip()
        ext_flag = f"--extensions {ext_input}" if ext_input else ""
    else:
        ext_flag = ""  # vai carregar extension.json

    # Executar pipeline
    cmd = f'python scripts/file_automation.py --folder_original "{folder_original}" --folder_organized "Organized files" {move_flag} {report_flags} {log_flag} {ext_flag}'
    print("\nExecutando comando:\n", cmd, "\n")
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    main()
