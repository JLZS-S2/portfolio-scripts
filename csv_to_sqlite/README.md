# CSV to SQLite Pipeline

## 📌 Visão Geral  
Este projeto automatiza a validação, limpeza e importação de arquivos **CSV** em bancos de dados **SQLite**.  
Ele detecta codificação, remove duplicados, trata valores nulos e gera relatórios estruturados em **JSON** e/ou **TXT**.  
O pipeline organiza os resultados em uma pasta dedicada `result/` e inclui logs estruturados para rastrear erros e o fluxo de execução.

👉 Em resumo: você coloca arquivos CSV na pasta `ENTRADA/`, e recebe bancos SQLite mais relatórios na pasta `result/`.

---

## 🚀 Funcionalidades
- Validação e abertura de arquivos CSV com detecção de codificação (**chardet**)  
- Importação de dados limpos para bancos SQLite  
- Remoção de duplicados e substituição de valores nulos por `"Not Informed"` (padrão)  
- Geração de relatórios em JSON e TXT  
- Logging estruturado em formato JSON ou TXT  
- Organização automática dos resultados na pasta `result/`  
- Rastreamento de erros com lista detalhada de arquivos que falharam  
- Launcher interativo (`launcher.py`) e script `.bat` para execução fácil  

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
csv_to_sqlite/
├── scripts/
│   ├── csv_to_sqlite.py
│   ├── logging_config.py
│   ├── logging_txt.py
│   ├── logging_config.json
│   └── __pycache__/
├── ENTRADA/
│   └── data.csv
├── result/
│   ├── report.json
│   ├── report.txt
│   ├── data.db
│   ├── process_txt.log
│   └── errors_txt.log
├── launcher.py
├── run_pipeline.bat
├── requirements.txt
└── LEIAME.txt
```

---

## ⚙️ Como Executar
1. Coloque seus arquivos CSV dentro da pasta `ENTRADA/`.  
2. Dê duplo clique em `run_pipeline.bat`.  
3. O launcher pedirá opções de personalização:
   - Valor para substituir nulos (padrão: `"Not Informed"`)  
   - Tipo de relatório (`txt` padrão, ou `json`)  
   - Tipo de log (`txt` padrão, ou `json`)  
   - Se você apenas apertar **Enter**, os valores padrão serão usados.  

---

## 📊 Exemplo de Saída

**Relatório JSON**
```json
{
  "report_title": "Report - CSV to SQLite",
  "date": "11/06/2026 11:30:00",
  "execution_time_seconds": 1.26,
  "summary": {
    "success": 1,
    "failures": 0,
    "failed_list": []
  },
  "file_records": [
    { "name": "data.csv", "records_inserted": 3, "duplicates_ignored": 1 }
  ],
  "notes": [
    "CSV imported into SQLite.",
    "Duplicates removed.",
    "Null values handled."
  ]
}
```

**Relatório TXT**
```text
Report - CSV to SQLite
Date: 11/06/2026 11:30:00
Execution time: 1.26 seconds

Execution Summary:
Success: 1
Failures: 0
Failed files: None

File Records:
- data.csv: Records inserted: 3 | Duplicates ignored: 1

Notes:
- CSV imported into SQLite.
- Duplicates removed.
- Null values handled.
```

---

## 🧠 Funções Internas (para desenvolvedores)
- `open_input()` → Valida e abre arquivos CSV com detecção de codificação  
- `duplicates_and_nulls()` → Remove duplicados e preenche valores nulos  
- `generate_report()` → Cria relatórios em JSON/TXT  
- `save_results()` → Move bancos, relatórios e logs para a pasta `result/`  
- `main()` → Controla o pipeline de execução  

---

## 🔒 Tratamento de Erros
- Detecta arquivos CSV ausentes ou inválidos  
- Lida com erros de codificação de forma segura  
- Rastreia arquivos que falharam com logging detalhado  
- Logs estruturados (`errors_json.log` ou `errors_txt.log`)  
- Logging crítico quando todos os arquivos falham  
- Serialização segura de tipos Pandas/NumPy em JSON  

---

## 📌 Tecnologias Utilizadas
- Python 3.12.7  
- Pandas  
- SQLite3  
- Argparse  
- Chardet para detecção de encoding  
- Logging / JSON logger  

---

## ✅ Resultado Final  
Este projeto é ideal para:
- Validação e limpeza de CSVs  
- Criação automatizada de bancos de dados  
- Pipelines de pré-processamento de dados  
- Automação de relatórios  
- Processamento em lote com rastreamento de erros  

---

## 🔎 Observações & Recomendações
- **save_results**: sobrescreve arquivos se já existirem em `result/`. Adicione timestamps se precisar de versionamento.  
- **Detecção de encoding**: pode ser imprecisa em arquivos muito pequenos.  
- **Duplicados**: removidos automaticamente; ajuste se quiser mantê-los.  
- **Defaults**: apertar Enter no launcher usa `"Not Informed"` para nulos, TXT para relatórios e TXT para logs.  
- **Exit codes**: atualmente não diferenciados. Adicionar `sys.exit(0/1)` melhora integração com CI/CD.  

---
