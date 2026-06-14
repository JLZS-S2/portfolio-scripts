# Weather Data Pipeline (Integração com API)

## 📌 Visão Geral  
Este projeto integra-se à API do **OpenWeather** para coletar dados meteorológicos de múltiplas cidades.  
Ele extrai campos relevantes, exporta resultados para **CSV** e **JSON**, e gera relatórios estruturados em **JSON** e/ou **TXT**.  
O pipeline organiza os resultados na pasta `result/` e inclui logs estruturados para rastrear erros e o fluxo de execução.

👉 Em resumo: você fornece uma lista de cidades e recebe dados meteorológicos + relatórios.

---

## 🚀 Funcionalidades
- **Integração** com a API OpenWeather  
- **Retry automático** (3 tentativas por cidade)  
- **Extração** de temperatura, umidade, descrição, vento, sensação térmica e pressão  
- **Exportação** para CSV e JSON  
- **Relatórios** em JSON e TXT  
- **Logging estruturado** em TXT ou JSON  
- **Suporte** a variáveis de ambiente via `.env`  
- **Saída organizada** na pasta `result/`  
- **Rastreamento de erros** com lista detalhada de cidades que falharam  

---

## 📋 Requisitos
- Windows com Python 3.12+  
- Dependências listadas em `requirements.txt`  
- Arquivo `.env` na raiz com:  
```
API_KEY=sua_chave_openweather
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

---

## 📂 Estrutura do Projeto
```
weather_pipeline/
├── scripts/
│   ├── weather_pipeline.py
│   ├── logging_config.py
│   ├── logging_txt.py
│   └── logging_config.json
├── requirements.txt
├── .env
├── ENTRADA/
│   └── cidades.txt
├── result/
│   └── (saídas geradas)
├── launcher.py
├── run_pipeline.bat
└── LEIAME.txt
```

---

## 🔄 Fluxo do Pipeline

```
+-----------+        +----------------+        +-----------+
|  ENTRADA  | -----> |   PROCESSO     | -----> |  RESULT   |
| (TXT)     |        | (weather_data) |        | (CSV+JSON+logs)|
+-----------+        +----------------+        +-----------+

ENTRADA: pasta já criada e entregue vazia
PROCESSO: leitura de cidades, requisições API, relatórios, logs
RESULT: CSV + JSON + relatórios + logs
```

⚠️ Observação:  
- Se a pasta **ENTRADA** estiver **vazia**, o pipeline não roda.  
- É obrigatório ter o arquivo **.env** com a `API_KEY`.  

---

## ⚙️ Como Executar

### Opção 1: Usando o menu interativo (`run_pipeline.bat`)
1. Coloque um arquivo TXT com nomes de cidades dentro da pasta ENTRADA.  
2. Crie o arquivo `.env` na raiz com sua chave da API.  
3. Clique duas vezes em **run_pipeline.bat**.  
4. O menu interativo será aberto:  
   - Escolha o arquivo TXT de cidades.  
   - Digite os nomes dos arquivos de saída (CSV e JSON).  
   - Escolha o tipo de relatório (TXT, JSON ou ambos).  
   - Escolha o tipo de log (TXT ou JSON).  
5. Aguarde a execução.  
6. Verifique os resultados na pasta **result\**.  

---

### Opção 2: Executar diretamente via linha de comando
Exemplo com saídas padrão:
```bash
python scripts/weather_pipeline.py --file_content ENTRADA/cidades.txt --json --txt
```

Saídas personalizadas:
```bash
python scripts/weather_pipeline.py --file_content ENTRADA/cidades.txt --file_csv clima.csv --file_json clima.json --txt
```

---

### Opções de Logging
- `--log_json` → logs estruturados em JSON  
- `--log_txt` → logs em texto simples (padrão)  

---

## 📊 Exemplo de Saída

**Relatório TXT**
```text
Report - Weather Data Pipeline
Date: 12/06/2026 14:20:00
Execution time: 1.25 seconds

Cities processed successfully: 5
Cities failed: 0
Failed cities: None

Notes:
- Weather data successfully retrieved from API.
- Data exported to CSV and JSON.
- Fallback applied for failed cities.
```

**Relatório JSON**
```json
{
  "report_title": "Report - Weather Data Pipeline",
  "date": "12/06/2026 14:20:00",
  "execution_time_seconds": 1.25,
  "summary": {
    "success": 5,
    "failures": 0,
    "failed_list": []
  },
  "notes": [
    "Weather data successfully retrieved from API.",
    "Data exported to CSV and JSON.",
    "Fallback applied for failed cities."
  ]
}
```

---

## 🧠 Funções Internas (para desenvolvedores)
- `request_api()` → faz requisições à API com retries  
- `extract_data()` → extrai campos relevantes da resposta da API  
- `generate_report()` → cria relatórios JSON/TXT  
- `save_results()` → move resultados e logs para `result/`  
- `main()` → controla o pipeline de execução  

---

## 🔒 Tratamento de Erros
- Detecta ausência de `API_KEY`  
- Lida com timeouts, erros de conexão e HTTP  
- Rastreia cidades que falharam com logging detalhado  
- Logs estruturados (`errors_json.log` ou `errors_txt.log`)  
- Exporta CSV/JSON vazio se todas as cidades falharem  

---

## 📌 Tecnologias Utilizadas
- Python 3.12.7  
- Requests  
- Pandas  
- Dotenv  
- Logging / RotatingFileHandler  
- python-json-logger  

---

## ✅ Resultado Final  
Este projeto é ideal para:
- Integração com APIs  
- Análise de dados meteorológicos  
- Automação de exportação de dados  
- Geração de relatórios  
- Pipelines com rastreamento de erros  

---

## 🔎 Observações & Recomendações
- **Sobrescrita de dados**: CSV e JSON são sobrescritos a cada execução. Adicione timestamps se precisar de versionamento.  
- **Limites da API**: a OpenWeather possui limites de requisição; para grandes lotes, considere adicionar delays.  
- **Encoding**: UTF-8 é usado para relatórios e saídas.  
- **Exit codes**: atualmente não diferenciados. Adicionar `sys.exit(0/1)` melhora integração com CI/CD.  

---
