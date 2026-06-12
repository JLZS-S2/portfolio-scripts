import os
import subprocess

def main():
    print("=== WEATHER DATA PIPELINE ===")
    print("Este menu ajuda você a configurar a execução sem precisar editar arquivos.")
    print()

    # Verifica se a pasta ENTRADA existe
    input_folder = "ENTRADA"
    if not os.path.exists(input_folder):
        print("❌ ERRO: Pasta ENTRADA não encontrada.")
        print("Crie a pasta ENTRADA e coloque seu arquivo TXT com nomes de cidades lá.")
        return

    # Lista arquivos TXT disponíveis
    input_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".txt")]
    if not input_files:
        print("❌ Nenhum arquivo TXT encontrado na pasta ENTRADA.")
        return

    print("Arquivos disponíveis na pasta ENTRADA:")
    for i, f in enumerate(input_files, 1):
        print(f"{i}. {f}")

    choice = input("\nDigite o número do arquivo que deseja usar: ").strip()
    try:
        file_choice = input_files[int(choice) - 1]
    except (ValueError, IndexError):
        print("❌ Escolha inválida.")
        return

    file_path = os.path.join(input_folder, file_choice)

    # Pergunta nomes dos arquivos de saída
    csv_name = input("Nome do arquivo CSV de saída [Data.csv]: ").strip() or "Data.csv"
    json_name = input("Nome do arquivo JSON de saída [Data.json]: ").strip() or "Data.json"

    # Pergunta tipo de relatório
    report_type = input("Tipo de relatório (txt/json) [txt]: ").strip().lower() or "txt"
    log_type = input("Tipo de log (txt/json) [txt]: ").strip().lower() or "txt"

    # Resumo antes da execução
    print("\nResumo da execução:")
    print(f"- Arquivo de cidades: {file_choice}")
    print(f"- Saída CSV: {csv_name}")
    print(f"- Saída JSON: {json_name}")
    print(f"- Relatório: {report_type}")
    print(f"- Log: {log_type}")
    print()

    args = [
        "python", "scripts/weather_pipeline.py",
        "--file_content", file_path,
        "--file_csv", csv_name,
        "--file_json", json_name
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
