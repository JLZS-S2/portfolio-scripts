import os
import subprocess

def listar_arquivos(extensao: str):
    entrada = "ENTRADA"
    arquivos = [f for f in os.listdir(entrada) if f.lower().endswith(extensao)]
    if not arquivos:
        print(f"❌ Nenhum arquivo {extensao} encontrado na pasta ENTRADA.")
    return arquivos

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
    print("PDF TO CSV PIPELINE - MENU INTERATIVO")
    print("========================================\n")

    # Extensão fixa: PDF
    extensao = ".pdf"
    arquivos = listar_arquivos(extensao)
    if not arquivos:
        print(f"❌ Nenhum arquivo {extensao} encontrado na pasta ENTRADA.")
        return

    print(f"Arquivos disponíveis em ENTRADA ({extensao}):")
    for i, f in enumerate(arquivos, 1):
        print(f"{i}. {f}")

    selecionados = input("Digite os números dos arquivos a processar (separados por espaço): ").split()
    escolhidos = []
    for s in selecionados:
        try:
            idx = int(s) - 1
            if 0 <= idx < len(arquivos):
                escolhidos.append(os.path.join("ENTRADA", arquivos[idx]))
        except ValueError:
            continue

    if not escolhidos:
        print("⚠️ Nenhum arquivo válido selecionado. Encerrando.")
        return

    # Nome do arquivo de saída
    output_csv = input("\nDigite o nome do CSV de saída [output.csv]: ").strip() or "output.csv"

    # Substituição de valores nulos
    null_replacement = input("Digite a string para substituir valores nulos [Not Informed]: ").strip() or "Not Informed"

    # Tipo de relatório
    relatorio = escolher_opcao(["TXT", "JSON", "Ambos"], "Escolha o tipo de relatório:", "TXT")
    if relatorio == "TXT":
        report_flags = "--txt"
    elif relatorio == "JSON":
        report_flags = "--json"
    else:
        report_flags = "--txt --json"

    # Tipo de log
    log = escolher_opcao(["TXT", "JSON"], "Escolha o tipo de log:", "TXT")
    log_flag = "--log_json" if log == "JSON" else "--log_txt"

    # Resumo das escolhas
    print("\n========================================")
    print("RESUMO DAS ESCOLHAS")
    print("========================================")
    print(f"Arquivos selecionados: {', '.join([os.path.basename(f) for f in escolhidos])}")
    print(f"Arquivo de saída: {output_csv}")
    print(f"Substituição de nulos: {null_replacement}")
    print(f"Relatório: {relatorio}")
    print(f"Log: {log}")
    print("========================================\n")

    # Montar comando
    cmd = f'python scripts/pdf_to_csv.py --files {" ".join(escolhidos)} --output "{output_csv}" --for_NaN "{null_replacement}" {report_flags} {log_flag}'
    print("🚀 Executando comando:\n", cmd, "\n")
    subprocess.run(cmd, shell=True)

    print("\n✅ Concluído! Verifique a pasta result/")

if __name__ == "__main__":
    main()
