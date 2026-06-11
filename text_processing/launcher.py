import os
import subprocess

def main():
    print("=== TEXT PROCESSING AUTOMATION ===")
    print("Este menu ajuda você a configurar a execução sem precisar editar arquivos.")
    print()

    # Lista todos os arquivos TXT da pasta ENTRADA
    input_folder = "ENTRADA"
    if not os.path.exists(input_folder):
        print("❌ ERRO: Pasta ENTRADA não encontrada.")
        print("Crie a pasta ENTRADA e coloque seus arquivos TXT lá.")
        return

    input_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.lower().endswith(".txt")]

    if not input_files:
        print("❌ Nenhum arquivo TXT encontrado na pasta ENTRADA.")
        return

    # Inputs opcionais
    keywords = input("Digite as palavras-chave para dividir o texto (separadas por espaço): ").split()
    report_type = input("Tipo de relatório (txt/json) [txt]: ").strip().lower() or "txt"
    log_type = input("Tipo de log (txt/json) [txt]: ").strip().lower() or "txt"

    # Resumo antes da execução
    print("\nResumo da execução:")
    print(f"- Arquivos TXT: {len(input_files)} encontrados")
    print(f"- Palavras-chave: {', '.join(keywords) if keywords else 'Nenhuma'}")
    print(f"- Relatório: {report_type}")
    print(f"- Log: {log_type}")
    print()

    args = [
        "python", "scripts/text_processing.py",
        "--file", *input_files,
        "--keywords", *keywords
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
