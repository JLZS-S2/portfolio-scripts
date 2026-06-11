import subprocess
import os

def main():
    print("=== CSV TO SQLITE ===")
    print("Este menu ajuda você a configurar a execução sem precisar editar arquivos.")
    print()

    # Lista todos os arquivos CSV da pasta ENTRADA
    input_folder = "ENTRADA"
    input_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.lower().endswith(".csv")]

    if not input_files:
        print("❌ Nenhum arquivo CSV encontrado na pasta ENTRADA.")
        return

    # Inputs opcionais: se o cliente só apertar Enter, usa o valor padrão
    null_value = input("Valor para substituir nulos [Não Informado]: ") or "Não Informado"
    report_type = input("Tipo de relatório (txt/json) [txt]: ").strip().lower() or "txt"
    log_type = input("Tipo de log (txt/json) [txt]: ").strip().lower() or "txt"

    args = [
        "python", "scripts/csv_to_sqlite.py",
        "--input", *input_files,
        "--for_NaN", null_value
    ]

    if report_type == "json":
        args.append("--json")
    else:
        args.append("--txt")

    if log_type == "json":
        args.append("--log_json")
    else:
        args.append("--log_txt")

    print("\nExecutando pipeline...")
    subprocess.run(args)

    print("\n✅ Concluído! Verifique a pasta result/")

if __name__ == "__main__":
    main()
