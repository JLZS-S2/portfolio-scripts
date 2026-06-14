# File Organizer Pipeline

## 📌 Visão Geral  
Este projeto automatiza a organização de arquivos por extensão.  
Ele move ou copia arquivos de uma pasta original para subpastas organizadas, conta arquivos por extensão, compacta a pasta organizada em um arquivo ZIP e gera relatórios estruturados em formato JSON e/ou TXT.  
O pipeline organiza os resultados em uma pasta dedicada `result/` e inclui logs estruturados para rastreamento de erros e fluxo de execução.

👉 Em resumo: você fornece uma pasta com arquivos, e recebe uma estrutura organizada mais relatórios.

---

## 🚀 Funcionalidades
- Organizar arquivos por extensão em subpastas  
- Tratar extensões não mapeadas em `OTHERS`  
- Mover ou copiar arquivos (padrão: copiar)  
- Contar arquivos por extensão com logging  
- Compactar a pasta organizada em ZIP  
- Geração de relatórios em JSON e TXT  
- Logging estruturado com arquivos rotativos  
- Saída organizada na pasta `result/`  
- Rastreamento de erros com lista detalhada de falhas  
- Mapeamento flexível de extensões via `extension.json` ou entrada manual  

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
file_automation/
├── scripts/
│   ├── file_automation.py
│   └── logging_config.json
│   ├── logging_config.py
│   ├── logging_txt.py
├── requirements.txt
├── extension.json
├── ENTRADA/
│   └── sample_files/
│       ├── file1.csv
│       ├── file2.txt
│       ├── image.png
│       └── doc.pdf
├── result/
│   └── (saídas geradas)
├── run_pipeline.bat
├── launcher.py
└── LEIAME.txt
```

---

## 🔄 Fluxo do Pipeline

```
+-----------+        +----------------+        +-----------+
|  ENTRADA  | -----> |   PROCESSO     | -----> |  RESULT   |
| (pastas)  |        | (file_automation)|      | (saídas)  |
+-----------+        +----------------+        +-----------+

ENTRADA: pasta já criada e entregue vazia
PROCESSO: organização, contagem, compactação, relatórios, logs
RESULT: pasta organizada + ZIP + relatórios + logs
```

⚠️ Observação:  
- Se a pasta **ENTRADA** estiver **vazia**, o pipeline não roda.  
- É necessário haver **ao menos uma pasta desorganizada** dentro de ENTRADA.  

---

## ⚙️ Como Executar

### Opção 1: Usando `extension.json`
Edite o arquivo `extension.json` para definir os mapeamentos:
```json
{
  "csv": "csv",
  "txt": "txt",
  "png": "images",
  "pdf": "docs"
}
```

Executar com cópia (padrão):
```bash
python scripts/file_automation.py --folder_original ENTRADA/sample_files --folder_organized "Organized files" --txt
```

Executar com mover:
```bash
python scripts/file_automation.py --folder_original ENTRADA/sample_files --folder_organized "Organized files" --move_files --json
```

---

### Opção 2: Mapeamento manual via `--extensions`
```bash
python scripts/file_automation.py --folder_original ENTRADA/sample_files --folder_organized "Organized files" --extensions csv:csv txt:txt png:images pdf:docs --txt
```

---

### Opções de Logging
- `--log_json` → logs estruturados em JSON  
- `--log_txt` → logs em texto simples (padrão)  

---

## 📊 Exemplo de Saída

**Relatório TXT**
```text
Report - File Organizer Pipeline
Date: 28/05/2026 16:40:00
Execution time: 0.55 seconds

Execution Summary:
Success: 1
Failures: 0
Failed items: None

File Counts:
- csv: 2 files
- txt: 1 files
- png: 1 files
- pdf: 1 files

Notes:
- Files organized by extension.
- Files counted by extension.
- Organized folder compressed into ZIP.
- Fallback applied for errors.
```

---

## 🧠 Funções Internas (para desenvolvedores)
- `organizer()` → Organiza arquivos por extensão  
- `counter()` → Conta arquivos por extensão  
- `zip_folder()` → Compacta a pasta organizada  
- `generate_report()` → Cria relatórios JSON/TXT  
- `save_results()` → Move resultados e logs para `result/`  
- `main()` → Controla o pipeline de execução  

---

## 🔒 Tratamento de Erros
- Detecta pastas ausentes ou vazias  
- Trata extensões não mapeadas  
- Rastreia itens com falha  
- Logs estruturados (`errors.log` ou `errors_txt.log`)  
- Logging crítico quando a execução falha  

---

## 📌 Tecnologias Utilizadas
- Python 3.12.7  
- Argparse  
- Logging / RotatingFileHandler  
- Zipfile  
- JSON  

---

## ✅ Resultado Final  
Este projeto é ideal para:
- Organização de arquivos  
- Processamento em lote  
- Arquivamento automatizado  
- Geração de relatórios  
- Pipelines com rastreamento de erros  

---

## 🔎 Observações & Recomendações
- **save_results**: sobrescreve arquivos se já existirem em `result/`. Adicione timestamps se precisar de versionamento.  
- **Pastas grandes**: a compactação pode demorar; considere dividir em partes.  
- **Exit codes**: atualmente não diferenciados. Adicionar `sys.exit(0/1)` melhora integração com CI/CD.  
- **Mapeamento de extensões**: você pode editar `extension.json` ou definir manualmente com `--extensions`.  

---
