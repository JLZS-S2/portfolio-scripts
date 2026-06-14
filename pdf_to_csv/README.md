# PDF to CSV Pipeline

## 📌 Visão Geral  
Este projeto automatiza a extração de tabelas e texto de arquivos **PDF**, convertendo-os em datasets **CSV** estruturados.  
Ele valida arquivos PDF, detecta separadores automaticamente, trata valores nulos e gera relatórios estruturados em **JSON** e/ou **TXT**.  
O pipeline organiza os resultados em uma pasta dedicada `result/` e inclui logs estruturados para rastreamento de erros e fluxo de execução.

👉 Em resumo: você fornece arquivos PDF e recebe um CSV mais relatórios.

---

## 🚀 Funcionalidades
- **Validação** de arquivos PDF (detecta ausentes, protegidos ou inválidos)  
- **Extração** de tabelas e texto das páginas PDF  
- **Detecção automática** de separadores em blocos de texto  
- **Conversão** dos dados extraídos em CSV  
- **Tratamento de valores nulos** com `"Not Informed"` ou string definida pelo usuário  
- **Relatórios** em JSON e TXT  
- **Logging estruturado** em TXT ou JSON  
- **Saída organizada** na pasta `result/`  
- **Rastreamento de erros** com lista detalhada de falhas  

---

## 📋 Requisitos
- Windows com Python 3.12+  
- Dependências listadas em `requirements.txt`  

Instale as dependências:
```bash
pip install -r requirements.txt
```

---

## 📂 Estrutura do Projeto
```
pdf_to_csv/
├── scripts/
│   └── pdf_to_csv.py
│   └── logging_config.json
│   ├── logging_config.py
│   ├── logging_txt.py
├── requirements.txt
├── ENTRADA/
│   └── (arquivos PDF)
├── result/
│   └── (saídas geradas)
├── run_pipeline.bat
├── launcher.py
├── LEIAME.txt
└── README.md
```

---

## 🔄 Fluxo do Pipeline

```
+-----------+        +----------------+        +-----------+
|  ENTRADA  | -----> |   PROCESSO     | -----> |  RESULT   |
| (PDFs)    |        | (pdf_to_csv)   |        | (CSV+logs)|
+-----------+        +----------------+        +-----------+

ENTRADA: pasta já criada e entregue vazia
PROCESSO: validação, extração, conversão, relatórios, logs
RESULT: CSV final + relatórios + logs
```

⚠️ Observação:  
- Se a pasta **ENTRADA** estiver **vazia**, o pipeline não roda.  
- Este pipeline funciona com **um ou mais arquivos PDF**.  

---

## ⚙️ Como Executar

### Opção 1: Usando o menu interativo (`run_pipeline.bat`)
1. Coloque seus arquivos PDF dentro da pasta ENTRADA.  
2. Clique duas vezes em **run_pipeline.bat**.  
3. O menu interativo será aberto:  
   - Escolha os arquivos PDF dentro de ENTRADA.  
   - Digite o nome do arquivo CSV de saída (padrão: `output.csv`).  
   - Digite a string para substituir valores nulos (`--for_NaN`, padrão: `"Not Informed"`).  
   - Escolha o tipo de relatório (TXT, JSON ou ambos).  
   - Escolha o tipo de log (TXT ou JSON).  
4. Aguarde a execução.  
5. Verifique os resultados na pasta **result\**.  

---

### Opção 2: Executar diretamente via linha de comando
Processar PDFs com relatório TXT (padrão):
```bash
python scripts/pdf_to_csv.py --files ENTRADA/sample1.pdf ENTRADA/sample2.pdf --txt
```

Gerar relatório JSON:
```bash
python scripts/pdf_to_csv.py --files ENTRADA/sample1.pdf ENTRADA/sample2.pdf --json
```

Substituição personalizada para valores nulos:
```bash
python scripts/pdf_to_csv.py --files ENTRADA/sample1.pdf ENTRADA/sample2.pdf --for_NaN "Unknown" --json --txt
```

---

### Opções de Logging
- `--log_json` → logs estruturados em JSON  
- `--log_txt` → logs em texto simples (padrão)  

---

## 📊 Exemplo de Saída

**Relatório TXT**
```text
Report - PDF to CSV
Date: 13/06/2026 18:30:00
Execution time: 0.75 seconds

Execution Summary:
Success: 2
Failures: 0
Failed files: None

File Records:
- output.csv: Records inserted: 250

Notes:
- PDF extracted into CSV.
- Tables and text processed.
- Null values handled.
```

**Relatório JSON**
```json
{
  "report_title": "Report - PDF to CSV",
  "date": "13/06/2026 18:30:00",
  "execution_time_seconds": 0.75,
  "summary": {
    "success": 2,
    "failures": 0,
    "failed_list": []
  },
  "file_records": [
    { "name": "output.csv", "records_inserted": 250 }
  ],
  "notes": [
    "PDF extracted into CSV.",
    "Tables and text processed.",
    "Null values handled."
  ]
}
```

---

## 🧠 Funções Internas (para desenvolvedores)
- `open_pdfs()` → valida arquivos PDF  
- `parse_text_block()` → detecta separadores e transforma texto em dicts  
- `type_identification()` → extrai tabelas ou texto dos PDFs  
- `null_values()` → substitui valores nulos no DataFrame  
- `generate_report()` → cria relatórios JSON/TXT  
- `save_results()` → move CSVs, relatórios e logs para `result/`  
- `main()` → controla o pipeline de execução  

---

## 🔒 Tratamento de Erros
- Detecta arquivos PDF ausentes, protegidos ou inválidos  
- Trata falhas na detecção de separadores com fallback para vírgula  
- Lista detalhada de arquivos que falharam  
- Logs estruturados (`errors_json.log` ou `errors_txt.log`)  
- Logging crítico quando todos os arquivos falham  

---

## 📌 Tecnologias Utilizadas
- Python 3.12.7  
- Pandas  
- pdfplumber  
- PyPDF  
- Argparse  
- Logging / RotatingFileHandler  
- python-json-logger  

---

## ✅ Resultado Final  
Este projeto é ideal para:
- Extração de tabelas/texto de PDFs  
- Geração automatizada de CSVs  
- Pipelines de limpeza de dados  
- Automação de relatórios  
- Processamento em lote com rastreamento de erros  

---

## 🔎 Observações & Recomendações
- **save_results**: sobrescreve arquivos se já existirem em `result/`. Adicione timestamps se precisar de versionamento.  
- **Detecção de separador**: pode falhar em blocos de texto irregulares; usa vírgula como padrão.  
- **Valores nulos**: substituídos automaticamente; ajuste a string conforme necessário.  
- **Exit codes**: atualmente não diferenciados. Adicionar `sys.exit(0/1)` melhora integração com CI/CD.  

---
