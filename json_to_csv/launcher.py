import subprocess
import os

def main():
    print("=== JSON TO CSV AUTOMATION ===")
    print("Este menu ajuda você a configurar a execução sem precisar editar arquivos.")
    print()

    # Lista todos os arquivos JSON da pasta ENTRADA
    input_folder = "ENTRADA"
    if not os.path.exists(input_folder):
        print("❌ ERRO: Pasta ENTRADA não encontrada.")
        print("Crie a pasta ENTRADA e coloque seus arquivos JSON lá.")
        return

    input_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.lower().endswith(".json")]

    if not input_files:
        print("❌ Nenhum arquivo JSON encontrado na pasta ENTRADA.")
        return

    # Inputs opcionais: se o cliente só apertar Enter, usa o valor padrão
    output_csv = input("Nome do arquivo CSV de saída [Merge.csv]: ") or "Merge.csv"
    report_type = input("Tipo de relatório (txt/json) [txt]: ").strip().lower() or "txt"
    log_type = input("Tipo de log (txt/json) [txt]: ").strip().lower() or "txt"
    null_value = input("Valor para substituir nulos [Not Informed]: ") or "Not Informed"

    # Resumo antes da execução
    print("\nResumo da execução:")
    print(f"- Arquivos JSON: {len(input_files)} encontrados")
    print(f"- Saída CSV: {output_csv}")
    print(f"- Relatório: {report_type}")
    print(f"- Log: {log_type}")
    print(f"- Substituição de nulos: {null_value}")
    print()

    args = [
        "python", "scripts/json_to_csv.py",
        "--json_files", *input_files,
        "--output_csv", output_csv,
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

    print("Executando pipeline...")
    subprocess.run(args)

    print("\n✅ Concluído! Verifique a pasta result/")

if __name__ == "__main__":
    main()
