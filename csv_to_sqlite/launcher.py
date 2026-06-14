import os
import subprocess

def main():
    print("========================================")
    print("CSV TO SQLITE PIPELINE - MENU INTERATIVO")
    print("========================================\n")

    # Lista todos os arquivos CSV da pasta ENTRADA
    input_folder = "ENTRADA"
    input_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.lower().endswith(".csv")]

    if not input_files:
        print("❌ Nenhum arquivo CSV encontrado na pasta ENTRADA.")
        return

    # Inputs opcionais
    null_value = input("Valor para substituir nulos [Não Informado]: ").strip() or "Não Informado"
    report_type = input("Tipo de relatório (txt/json/ambos) [txt]: ").strip().lower() or "txt"
    log_type = input("Tipo de log (txt/json) [txt]: ").strip().lower() or "txt"

    args = [
        "python", "scripts/csv_to_sqlite.py",
        "--input", *input_files,
        "--for_NaN", null_value
    ]

    if report_type == "json":
        args.append("--json")
    elif report_type == "ambos":
        args.extend(["--json", "--txt"])
    else:
        args.append("--txt")

    if log_type == "json":
        args.append("--log_json")
    else:
        args.append("--log_txt")

    # Resumo das escolhas
    print("\n========================================")
    print("RESUMO DAS ESCOLHAS")
    print("========================================")
    print(f"Arquivos selecionados: {', '.join([os.path.basename(f) for f in input_files])}")
    print(f"Substituição de nulos: {null_value}")
    print(f"Relatório: {report_type}")
    print(f"Log: {log_type}")
    print("========================================\n")

    print("🚀 Executando pipeline...\n")
    subprocess.run(args)

    print("\n✅ Concluído! Verifique a pasta result/")

if __name__ == "__main__":
    main()
