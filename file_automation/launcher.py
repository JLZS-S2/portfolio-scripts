import os
import subprocess

def listar_pastas_entrada():
    entrada = "ENTRADA"
    pastas = [p for p in os.listdir(entrada) if os.path.isdir(os.path.join(entrada, p))]
    if not pastas:
        print("❌ Nenhuma pasta encontrada dentro de ENTRADA.")
    return pastas

def escolher_opcao(opcoes, mensagem, padrao=None):
    print("\n" + mensagem)
    for i, opcao in enumerate(opcoes, 1):
        print(f"{i}. {opcao}")
    escolha = input("Digite o número da opção desejada: ").strip()
    try:
        idx = int(escolha) - 1
        if 0 <= idx < len(opcoes):
            return opcoes[idx]
    except ValueError:
        pass
    print(f"⚠️ Opção inválida. Usando padrão: {padrao or opcoes[0]}")
    return padrao or opcoes[0]

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
    acao = escolher_opcao(["Copiar arquivos", "Mover arquivos"], "Deseja copiar ou mover os arquivos?", "Copiar arquivos")
    move_flag = "--move_files" if acao == "Mover arquivos" else "--copy_files"

    # Escolher tipo de relatório
    relatorio = escolher_opcao(["TXT", "JSON", "Ambos"], "Escolha o tipo de relatório:", "TXT")
    if relatorio == "TXT":
        report_flags = "--txt"
    elif relatorio == "JSON":
        report_flags = "--json"
    else:
        report_flags = "--txt --json"

    # Escolher tipo de log
    log = escolher_opcao(["TXT", "JSON"], "Escolha o tipo de log:", "TXT")
    log_flag = "--log_json" if log == "JSON" else "--log_txt"

    # Escolher se usa extension.json ou manual
    ext_choice = escolher_opcao(["Usar extension.json", "Definir manualmente"], "Deseja usar o extension.json ou definir manualmente?", "Usar extension.json")
    if ext_choice == "Definir manualmente":
        print("Digite os mapeamentos no formato EXT:PASTA separados por espaço (ex: csv:csv txt:txt png:images pdf:docs)")
        ext_input = input("Mapeamentos: ").strip()
        ext_flag = f"--extensions {ext_input}" if ext_input else ""
    else:
        ext_flag = ""  # vai carregar extension.json

    # Resumo das escolhas
    print("\n========================================")
    print("RESUMO DAS ESCOLHAS")
    print("========================================")
    print(f"Pasta escolhida: {folder_original}")
    print(f"Ação: {acao}")
    print(f"Relatório: {relatorio}")
    print(f"Log: {log}")
    print(f"Extensões: {'extension.json' if not ext_flag else ext_flag}")
    print("========================================\n")

    # Executar pipeline
    cmd = f'python scripts/file_automation.py --folder_original "{folder_original}" --folder_organized "Organized files" {move_flag} {report_flags} {log_flag} {ext_flag}'
    print("🚀 Executando comando:\n", cmd, "\n")
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    main()
