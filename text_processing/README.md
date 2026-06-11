# Text Processing Automation

## 📌 Visão Geral  
Este projeto automatiza a limpeza e o processamento de arquivos **TXT**.  
Ele remove linhas em branco, divide o conteúdo por múltiplas palavras-chave, conta linhas e palavras e gera relatórios estruturados em **JSON** e/ou **TXT**.  
O pipeline organiza os resultados em uma pasta dedicada `result/` e inclui logs estruturados para rastrear erros e o fluxo de execução.

👉 Em resumo: você fornece arquivos TXT e recebe arquivos limpos/divididos mais relatórios.

---

## 🚀 Funcionalidades
- Remoção automática de linhas em branco  
- Divisão de texto por palavras-chave (suporta múltiplas)  
- Contagem de linhas e palavras por arquivo  
- Geração de relatórios em JSON e TXT  
- Logging estruturado com arquivos rotativos (JSON ou TXT)  
- Saída organizada na pasta `result/`  
- Detecção de codificação com **chardet**  
- Rastreamento de erros com lista detalhada de arquivos que falharam  

---

## 📋 Requisitos
- Python 3.12+  
- Dependências listadas em `requirements.txt`  

Instale as dependências:
```bash
pip install -r requirements.txt
```

---

## 📂 Estrutura do Projeto
```
text_processing/
├── scripts/
│   ├── text_processing.py
│   ├── logging_config.py
│   ├── logging_txt.py
│   └── logging_config.json
├── requirements.txt
├── ENTRADA/
│   ├── sample1.txt
│   └── sample2.txt
├── result/
│   ├── report.json
│   ├── report.txt
│   ├── cleaned_files/
│   │   ├── new_sample1.txt
│   │   └── new_sample2.txt
│   ├── process_txt.log
│   └── errors_txt.log
├── launcher.py
├── run_pipeline.bat
└── LEIAME.txt
```

---

## ⚙️ Como Executar
Arquivo único:
```bash
python scripts/text_processing.py --file sample1 --keywords DATA WORD --json --txt
```

Múltiplos arquivos:
```bash
python scripts/text_processing.py --file sample1 sample2 --keywords DATA KEY --txt
```

Opções de logging:
- `--log_json` → logs estruturados em JSON  
- `--log_txt` → logs em texto simples (default)  

---

## 📊 Exemplo de Saída

**Relatório JSON**
```json
{
  "report_title": "Report - Text Processing Automation",
  "date": "01/06/2026 21:30:00",
  "execution_time_seconds": 0.42,
  "files": {
    "new_sample1.txt": { "lines": 12, "words": 95 },
    "new_sample2.txt": { "lines": 8, "words": 60 }
  },
  "summary": {
    "success": 2,
    "failures": 0,
    "failed_list": []
  },
  "notes": [
    "All files were cleaned and split by keyword.",
    "Reports generated in JSON and TXT formats.",
    "Files moved to organized folders.",
    "Fallback applied for errors."
  ]
}
```

**Relatório TXT**
```text
Report - Text Processing Automation
Date: 01/06/2026 21:30:00
Execution time: 0.42 seconds

Summary of processed files:
- new_sample1.txt: 12 lines, 95 words
- new_sample2.txt: 8 lines, 60 words

Execution Summary:
Files processed successfully: 2
Files failed: 0
Failed files: None

Notes:
- All files were cleaned and split by keyword.
- Reports generated in JSON and TXT formats.
- Files moved to organized folders.
- Fallback applied for errors.
```

---

## 🧠 Funções Internas (para desenvolvedores)
- `clean_text()` → Remove linhas em branco e detecta encoding  
- `split_keywords()` → Divide texto usando múltiplas palavras-chave  
- `count_lines_words()` → Conta linhas e palavras por arquivo  
- `generate_report()` → Cria relatórios em JSON/TXT  
- `save_results()` → Move resultados e logs para a pasta `result/`  
- `main()` → Controla o pipeline de execução  

---

## 🔒 Tratamento de Erros
- Detecta erros de codificação com **chardet**  
- Lida com arquivos TXT inválidos ou ilegíveis  
- Rastreia arquivos que falharam com logging detalhado  
- Logs estruturados (`errors_json.log` ou `errors_txt.log`)  
- Logging crítico quando todos os arquivos falham  

---

## 📌 Tecnologias Utilizadas
- Python 3.12.7  
- Argparse  
- Logging / RotatingFileHandler  
- JSON / Regex  
- Chardet para detecção de encoding  
- python-json-logger  

---

## ✅ Resultado Final  
Este projeto é ideal para:
- Automação de processamento de texto  
- Processamento em lote de arquivos TXT  
- Limpeza de dados  
- Geração de relatórios  
- Pipelines com rastreamento de erros  

---

## 🔎 Observações & Recomendações
- **save_results**: sobrescreve arquivos se já existirem em `result/`. Adicione timestamps se precisar de versionamento.  
- **Palavras-chave**: escolha com cuidado para evitar divisões excessivas.  
- **Detecção de encoding**: pode ser imprecisa em arquivos muito pequenos.  
- **Exit codes**: atualmente não diferenciados. Adicionar `sys.exit(0/1)` melhora integração com CI/CD.  

---
