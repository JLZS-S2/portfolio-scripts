import os
import subprocess

def listar_csv_entrada():
    entrada = "ENTRADA"
    if not os.path.exists(entrada):
        print("❌ ERRO: Pasta ENTRADA não encontrada.")
        return []
    return [f for f in os.listdir(entrada) if f.lower().endswith(".csv")]

def escolher_opcao(opcoes, mensagem):
    print("\n" + mensagem)
    for i, opcao in enumerate(opcoes, 1):
        print(f"{i}. {opcao}")
    escolha = input("Digite o número da opção desejada: ")
    try:
        idx = int(escolha) - 1
        if 0 <= idx < len(opcoes):
            return opcoes[idx]
    except ValueError:
        pass
    print("⚠️ Opção inválida. Usando padrão:", opcoes[0])
    return opcoes[0]

def main():
    print("========================================")
    print("MERGE & FILTER CSV PIPELINE - MENU INTERATIVO")
    print("========================================\n")

    # Escolher arquivos CSV
    csv_files = listar_csv_entrada()
    if not csv_files:
        print("❌ Nenhum arquivo CSV encontrado na pasta ENTRADA.")
        return

    print("Arquivos CSV disponíveis em ENTRADA:")
    for i, f in enumerate(csv_files, 1):
        print(f"{i}. {f}")
    selecionados = input("Digite os números dos arquivos a processar (separados por espaço): ").split()
    escolhidos = []
    for s in selecionados:
        try:
            idx = int(s) - 1
            if 0 <= idx < len(csv_files):
                escolhidos.append(os.path.join("ENTRADA", csv_files[idx]))
        except ValueError:
            continue
    if not escolhidos:
        print("⚠️ Nenhum arquivo válido selecionado. Encerrando.")
        return

    # Nome do arquivo de saída
    output_csv = input("\nDigite o nome do CSV de saída [output.csv]: ").strip() or "output.csv"

    # Substituição de valores nulos
    null_replacement = input("Digite a string para substituir valores nulos [Not Informed]: ").strip() or "Not Informed"

    # Aplicar filtros?
    filtro = escolher_opcao(["Sim", "Não"], "Aplicar filtros do filter.json?")
    filtro_flag = "--filter" if filtro == "Sim" else ""

    # Tipo de relatório
    relatorio = escolher_opcao(["TXT", "JSON", "Ambos"], "Escolha o tipo de relatório:")
    if relatorio == "TXT":
        report_flags = "--txt"
    elif relatorio == "JSON":
        report_flags = "--json"
    else:
        report_flags = "--txt --json"

    # Tipo de log
    log = escolher_opcao(["TXT", "JSON"], "Escolha o tipo de log:")
    log_flag = "--log_json" if log == "JSON" else "--log_txt"

    # Resumo das escolhas
    print("\n========================================")
    print("RESUMO DAS ESCOLHAS")
    print("========================================")
    print(f"Arquivos selecionados: {', '.join([os.path.basename(f) for f in escolhidos])}")
    print(f"Arquivo de saída: {output_csv}")
    print(f"Substituição de nulos: {null_replacement}")
    print(f"Aplicar filtros: {filtro}")
    print(f"Relatório: {relatorio}")
    print(f"Log: {log}")
    print("========================================\n")

    # Montar comando
    cmd = f'python scripts/merge_filter_csv.py --files_csv {" ".join(escolhidos)} --output_csv "{output_csv}" --for_NaN "{null_replacement}" {filtro_flag} {report_flags} {log_flag}'
    print("🚀 Executando comando:\n", cmd, "\n")
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    main()
