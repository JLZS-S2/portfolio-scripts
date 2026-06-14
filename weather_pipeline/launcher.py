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
    print("WEATHER DATA PIPELINE - MENU INTERATIVO")
    print("========================================\n")

    # Extensão fixa: TXT
    extensao = ".txt"
    arquivos = listar_arquivos(extensao)
    if not arquivos:
        print(f"❌ Nenhum arquivo {extensao} encontrado na pasta ENTRADA.")
        return

    print(f"Arquivos disponíveis em ENTRADA ({extensao}):")
    for i, f in enumerate(arquivos, 1):
        print(f"{i}. {f}")

    escolha = input("Digite o número do arquivo a processar: ").strip()
    try:
        idx = int(escolha) - 1
        if 0 <= idx < len(arquivos):
            file_path = os.path.join("ENTRADA", arquivos[idx])
        else:
            print("⚠️ Escolha inválida. Encerrando.")
            return
    except ValueError:
        print("⚠️ Escolha inválida. Encerrando.")
        return

    # Nomes dos arquivos de saída
    csv_name = input("\nDigite o nome do arquivo CSV de saída [Data.csv]: ").strip() or "Data.csv"
    json_name = input("Digite o nome do arquivo JSON de saída [Data.json]: ").strip() or "Data.json"

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
    print(f"Arquivo de cidades: {os.path.basename(file_path)}")
    print(f"Saída CSV: {csv_name}")
    print(f"Saída JSON: {json_name}")
    print(f"Relatório: {relatorio}")
    print(f"Log: {log}")
    print("========================================\n")

    # Montar comando
    cmd = f'python scripts/weather_pipeline.py --file_content "{file_path}" --file_csv "{csv_name}" --file_json "{json_name}" {report_flags} {log_flag}'
    print("🚀 Executando comando:\n", cmd, "\n")
    subprocess.run(cmd, shell=True)

    print("\n✅ Concluído! Verifique a pasta result/")

if __name__ == "__main__":
    main()
