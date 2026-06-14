# Merge & Filter CSV Pipeline

## 📌 Visão Geral  
Este projeto automatiza a junção de múltiplos arquivos **CSV** em um único dataset.  
Ele remove duplicados, trata valores nulos, aplica filtros dinâmicos definidos em um arquivo JSON e gera relatórios estruturados em **JSON** e/ou **TXT**.  
O pipeline organiza os resultados em uma pasta dedicada `result/` e inclui logs estruturados para rastreamento de erros e fluxo de execução.

👉 Em resumo: você fornece arquivos CSV e recebe um CSV limpo/filtrado mais relatórios.

---

## 🚀 Funcionalidades
- **Leitura** de múltiplos arquivos CSV de uma vez  
- **Junção** em um único dataset  
- **Remoção de duplicados** automaticamente  
- **Tratamento de valores nulos** com `"Not Informed"` ou string definida pelo usuário  
- **Aplicação de filtros** dinâmicos definidos em `filter.json`  
- **Exportação** do arquivo CSV final  
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
merge_filter_csv/
├── scripts/
│   ├── merge_filter_csv.py
│   ├── logging_config.py
│   ├── logging_txt.py
│   └── logging_config.json
├── requirements.txt
├── filter.json
├── ENTRADA/
│   ├── file1.csv
│   ├── file2.csv
│   └── file3.csv
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
| (CSV)     |        | (merge_filter) |        | (CSV + logs)|
+-----------+        +----------------+        +-----------+

ENTRADA: pasta já criada e entregue vazia
PROCESSO: junção, remoção de duplicados, filtros, relatórios, logs
RESULT: CSV final + relatórios + logs
```

⚠️ Observação:  
- Se a pasta **ENTRADA** estiver **vazia**, o pipeline não roda.  
- Este pipeline exige **pelo menos 2 arquivos CSV** para funcionar.  

---

## ⚙️ Como Executar

### Opção 1: Usando o menu interativo (`run_pipeline.bat`)
1. Coloque seus arquivos CSV dentro da pasta ENTRADA.  
2. Clique duas vezes em **run_pipeline.bat**.  
3. O menu interativo será aberto:  
   - Escolha os arquivos CSV dentro de ENTRADA.  
   - Digite o nome do arquivo de saída (padrão: `output.csv`).  
   - Digite a string para substituir valores nulos (`--for_NaN`, padrão: `"Not Informed"`).  
   - Escolha se deseja aplicar filtros do `filter.json`.  
   - Escolha o tipo de relatório (TXT, JSON ou ambos).  
   - Escolha o tipo de log (TXT ou JSON).  
4. Aguarde a execução.  
5. Verifique os resultados na pasta **result\**.  

---

### Opção 2: Executar diretamente via linha de comando
Sem filtros:
```bash
python scripts/merge_filter_csv.py --files_csv ENTRADA/file1.csv ENTRADA/file2.csv ENTRADA/file3.csv --output_csv merged.csv --txt
```

Com filtros:
```bash
python scripts/merge_filter_csv.py --files_csv ENTRADA/file1.csv ENTRADA/file2.csv ENTRADA/file3.csv --output_csv filtered.csv --filter --json
```

---

### Opções de Logging
- `--log_json` → logs estruturados em JSON  
- `--log_txt` → logs em texto simples (padrão)  

---

## 🔎 Configuração de Filtros
Os filtros são definidos pelo usuário em um arquivo JSON (`filter.json`).  
O script lê este arquivo e aplica as regras ao DataFrame final.

⚠️ Importante: os nomes das colunas no JSON devem ser **idênticos** aos nomes das colunas no CSV — incluindo maiúsculas/minúsculas e ortografia.

**Exemplo filter.json**
```json
{
  "filters": [
    { "column": "Country", "operator": "==", "value": "Brazil" },
    { "column": "Age", "operator": ">", "value": 25 }
  ]
}
```

**Operadores suportados**
- `==` → igualdade  
- `> < >= <=` → comparações numéricas  
- `contains` → busca parcial em texto  

---

## 📊 Exemplo de Saída

**Relatório TXT**
```text
Report - Merge & Filter Pipeline
Date: 13/06/2026 13:30:00
Execution time: 0.45 seconds

Execution Summary:
Success: 3
Failures: 0
Failed files: None

Notes:
- CSV files merged.
- Filters applied if provided.
- Null values handled.
```

**Relatório JSON**
```json
{
  "report_title": "Report - Merge & Filter Pipeline",
  "date": "13/06/2026 13:30:00",
  "execution_time_seconds": 0.45,
  "summary": {
    "success": 3,
    "failures": 0,
    "failed_list": []
  },
  "notes": [
    "CSV files merged.",
    "Filters applied if provided.",
    "Null values handled."
  ]
}
```

---

## 🧠 Funções Internas (para desenvolvedores)
- `open_input()` → abre e valida arquivos CSV  
- `clean_and_merge()` → remove duplicados e trata valores nulos  
- `apply_filter()` → aplica filtros do `filter.json`  
- `generate_report()` → cria relatórios JSON/TXT  
- `save_results()` → move resultados e logs para `result/`  
- `main()` → controla o pipeline de execução  

---

## 🔒 Tratamento de Erros
- Detecta arquivos CSV ausentes ou inválidos  
- Aplica filtros inválidos de forma segura (ignora e loga)  
- Lista detalhada de arquivos que falharam  
- Logs estruturados (`errors_json.log` ou `errors_txt.log`)  
- Logging crítico quando todos os arquivos falham  

---

## 📌 Tecnologias Utilizadas
- Python 3.12.7  
- Pandas  
- Argparse  
- Logging / RotatingFileHandler  
- python-json-logger  

---

## ✅ Resultado Final  
Este projeto é ideal para:
- Limpeza e pré-processamento de dados  
- Junção em lote de arquivos CSV  
- Pipelines automatizados de filtragem  
- Automação de relatórios  
- Processamento em lote com rastreamento de erros  

---

## 🔎 Observações & Recomendações
- **save_results**: sobrescreve arquivos se já existirem em `result/`. Adicione timestamps se precisar de versionamento.  
- **Filtros**: garanta que os nomes das colunas sejam idênticos aos do CSV.  
- **Duplicados**: são removidos automaticamente. Ajuste se quiser mantê-los.  
- **Exit codes**: atualmente não diferenciados. Adicionar `sys.exit(0/1)` melhora integração com CI/CD.  

---
