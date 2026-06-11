# JSON to CSV Automation

## 📌 Visão Geral
Este projeto automatiza a conversão de arquivos **JSON** em um único arquivo **CSV**.  
Ele valida múltiplos formatos de JSON (padrão, JSONL, dict/list), trata valores nulos e gera relatórios estruturados em **JSON** e/ou **TXT**.  
O pipeline organiza todos os resultados em uma pasta dedicada `result/` e inclui logs para rastrear erros e o fluxo de execução.

👉 Em resumo: você fornece arquivos JSON e recebe um CSV limpo mais relatórios.

---

## 🚀 Funcionalidades
- Leitura de múltiplos arquivos JSON de uma vez  
- Suporte a JSON, JSONL e estruturas dict/list  
- Detecção automática de codificação com **chardet**  
- Substituição de valores nulos por `"Not Informed"` (ou valor definido pelo usuário)  
- Concatenação em um único arquivo CSV  
- Geração de relatórios em JSON e TXT  
- Logging estruturado para rastrear execução e erros  
- Organização automática dos resultados na pasta `result/`  
- Lista detalhada de arquivos que falharam na leitura  

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
```bash
json_to_csv/
├── scripts/
│   ├── json_to_csv.py
│   ├── logging_config.py
│   ├── logging_txt.py
│   └── logging_config.json
├── requirements.txt
├── ENTRADA/              # Pasta para colocar os arquivos JSON
├── result/               # Pasta onde os resultados serão salvos
├── run_pipeline.bat      # Arquivo para iniciar o processo
├── launcher.py           # Menu interativo
└── LEIAME.txt            # Instruções rápidas
```

---

## ⚙️ Como Executar
Arquivo único:
```bash
python scripts/json_to_csv.py --json_files data1 --output_csv output.csv --json --txt
```

Múltiplos arquivos:
```bash
python scripts/json_to_csv.py --json_files data1 data2 data3 --output_csv clientes.csv --txt
```

Opções de logging:
- **--log_json** → logs estruturados em JSON  
- **--log_txt** → logs em texto simples (default)  

---

## 📊 Exemplo de Saída
Relatório JSON:
```json
{
  "report_title": "Report - JSON to CSV Automation",
  "date": "26/05/2026 15:40:00",
  "execution_time_seconds": 0.35,
  "files_success": 3,
  "files_failed": 0,
  "failed_list": [],
  "notes": [
    "JSON files processed and concatenated.",
    "Null values handled.",
    "Final CSV generated successfully."
  ]
}
```

Relatório TXT:
```text
Report - JSON to CSV Automation
Date: 26/05/2026 15:40:00
Execution time: 0.35 seconds

Files processed successfully: 3
Files failed: 0
Failed files: None

Notes:
- JSON files processed and concatenated.
- Null values handled.
- Final CSV generated successfully.
```

---

## 🧠 Funções Internas (para desenvolvedores)
- **open_json()** → Abre e valida arquivos JSON com estratégias de fallback  
- **handle_null_values()** → Substitui valores nulos por `"Not Informed"`  
- **generate_report()** → Cria relatórios em JSON/TXT  
- **save_results()** → Move resultados e logs para a pasta `result/`  
- **main()** → Controla o pipeline de execução  

---

## 🔒 Tratamento de Erros
- Detecta erros de codificação com **chardet**  
- Lida com formatos inválidos de JSON (padrão, JSONL, dict/list)  
- Rastreia arquivos que falharam com logging detalhado  
- Logs estruturados (`errors_json.log` ou `errors_txt.log`)  
- Logging crítico quando todos os arquivos falham  

---

## 📌 Tecnologias Utilizadas
- Python 3.12.7  
- Pandas  
- Chardet  
- Argparse  
- Logging / RotatingFileHandler  
- python-json-logger  

---

## ✅ Resultado Final
Este projeto é ideal para:
- Pipelines de conversão de dados  
- Validação de JSONs  
- Geração de CSVs consolidados  
- Automação de relatórios  
- Processamento em lote com rastreamento de erros  

---

## 🔎 Observações & Recomendações
- **Detecção de encoding**: o chardet pode ser impreciso em arquivos muito pequenos.  
- **Concatenação**: JSONs com estruturas diferentes geram muitas colunas com nulos.  
- **save_results**: sobrescreve arquivos se já existirem na pasta `result/`. Adicione timestamps se precisar de versionamento.  
- **Validação de schema**: não é aplicada. Adicione verificações se precisar de consistência entre JSONs.  
- **Duplicados**: não são removidos. Use `drop_duplicates()` se necessário.  
- **Exit codes**: não diferenciados. Adicionar `sys.exit(0/1)` pode melhorar integração com CI/CD.  
- **Performance**: para grandes volumes de JSONs, considere usar chunks do Pandas para otimizar memória.  

---