# JSON to CSV Automation

## 📌 Visão Geral  
Este projeto automatiza a conversão de arquivos **JSON** em um único arquivo **CSV**.  
Ele valida múltiplos formatos de JSON (padrão, JSONL, dict/list), trata valores nulos e gera relatórios estruturados em **JSON** e/ou **TXT**.  
O pipeline organiza os resultados em uma pasta dedicada `result/` e inclui logs estruturados para rastreamento de erros e fluxo de execução.

👉 Em resumo: você fornece arquivos JSON e recebe um CSV consolidado mais relatórios.

---

## 🚀 Funcionalidades
- **Validação** de arquivos JSON (padrão, JSONL, dict/list)  
- **Processamento** dos dados (concatenação em CSV único)  
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
json_to_csv/
├── scripts/
│   ├── json_to_csv.py
│   ├── logging_config.py
│   ├── logging_txt.py
│   └── logging_config.json
├── requirements.txt
├── ENTRADA/
│   └── (arquivos JSON)
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
|  ENTRADA  | -----> |   PROCESSO     | -----> |  RESULT     |
| (JSONs)   |        | (json_to_csv)  |        | (CSV + logs)|
+-----------+        +----------------+        +-----------+

ENTRADA: pasta já criada e entregue vazia
PROCESSO: validação, concatenação, relatórios, logs
RESULT: CSV final + relatórios + logs
```

⚠️ Observação:  
- Se a pasta **ENTRADA** estiver **vazia**, o pipeline não roda.  
- Este pipeline funciona com **um ou mais arquivos JSON**.  

---

## ⚙️ Como Executar

### Opção 1: Usando o menu interativo (`run_pipeline.bat`)
1. Coloque seus arquivos JSON dentro da pasta ENTRADA.  
2. Clique duas vezes em **run_pipeline.bat**.  
3. O menu interativo será aberto:  
   - Escolha os arquivos dentro de ENTRADA.  
   - Digite o nome do arquivo CSV de saída (padrão: `Merge.csv`).  
   - Digite a string para substituir valores nulos (`--for_NaN`, padrão: `"Not Informed"`).  
   - Escolha o tipo de relatório (TXT, JSON ou ambos).  
   - Escolha o tipo de log (TXT ou JSON).  
4. Aguarde a execução.  
5. Verifique os resultados na pasta **result\**.  

---

### Opção 2: Executar diretamente via linha de comando
```bash
python scripts/json_to_csv.py --json_files ENTRADA/data1.json ENTRADA/data2.json --output_csv resultado.csv --txt
```

Com relatório JSON:
```bash
python scripts/json_to_csv.py --json_files ENTRADA/data.json --output_csv resultado.csv --json
```

---

### Opções de Logging
- `--log_json` → logs estruturados em JSON  
- `--log_txt` → logs em texto simples (padrão)  

---

## 📊 Exemplo de Saída

**Relatório TXT**
```text
Report - JSON to CSV Automation
Date: 14/06/2026 14:20:00
Execution time: 0.35 seconds

Execution Summary:
Success: 3
Failures: 0
Failed files: None

Notes:
- JSON files processed and concatenated.
- Null values handled.
- Final CSV generated successfully.
```

**Relatório JSON**
```json
{
  "report_title": "Report - JSON to CSV Automation",
  "date": "14/06/2026 14:20:00",
  "execution_time_seconds": 0.35,
  "summary": {
    "success": 3,
    "failures": 0,
    "failed_list": []
  },
  "notes": [
    "JSON files processed and concatenated.",
    "Null values handled.",
    "Final CSV generated successfully."
  ]
}
```

---

## 🧠 Funções Internas (para desenvolvedores)
- `open_json()` → valida e abre arquivos JSON  
- `handle_null_values()` → substitui valores nulos  
- `generate_report()` → cria relatórios JSON/TXT  
- `save_results()` → move resultados e logs para `result/`  
- `main()` → controla o pipeline de execução  

---

## 🔒 Tratamento de Erros
- Detecta erros de codificação com **chardet**  
- Lida com formatos inválidos de JSON  
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
- Conversão de JSONs em CSV  
- Consolidação de múltiplos arquivos em um único dataset  
- Automação de relatórios  
- Processamento em lote com rastreamento de erros  

---

## 🔎 Observações & Recomendações
- **Detecção de encoding**: pode ser imprecisa em arquivos muito pequenos.  
- **Concatenação**: JSONs com estruturas diferentes geram muitas colunas com nulos.  
- **save_results**: sobrescreve arquivos se já existirem em `result/`. Adicione timestamps se precisar de versionamento.  
- **Validação de schema**: não é aplicada; adicione verificações se precisar de consistência entre JSONs.  
- **Exit codes**: atualmente não diferenciados. Adicionar `sys.exit(0/1)` melhora integração com CI/CD.  
- **Performance**: para grandes volumes de JSONs, considere usar chunks do Pandas para otimizar memória.  

---
