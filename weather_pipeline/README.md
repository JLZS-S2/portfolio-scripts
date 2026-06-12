# Weather Data Pipeline (Integração com API)

## 📌 Visão Geral  
Este projeto integra-se à API do **OpenWeather** para coletar dados meteorológicos de múltiplas cidades.  
Ele extrai campos relevantes, exporta resultados para **CSV** e **JSON**, e gera relatórios estruturados em **JSON** e/ou **TXT**.  
O pipeline organiza os resultados na pasta `result/` e inclui logs estruturados para rastrear erros e o fluxo de execução.

👉 Em resumo: você fornece uma lista de cidades e recebe dados meteorológicos + relatórios.

---

## 🚀 Funcionalidades
- Integração com a API OpenWeather  
- Mecanismo de retry (3 tentativas por cidade)  
- Extração de temperatura, umidade, descrição, velocidade do vento, sensação térmica e pressão  
- Exportação para CSV e JSON  
- Geração de relatórios em JSON e TXT  
- Logging estruturado com arquivos rotativos (JSON ou TXT)  
- Suporte a variáveis de ambiente via `.env`  
- Saída organizada na pasta `result/`  
- Rastreamento de erros com lista detalhada de cidades que falharam  

---

## 📋 Requisitos
- Python 3.12+  
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
│   ├── report.json
│   ├── report.txt
│   ├── Data.csv
│   ├── Data.json
│   ├── process_txt.log
│   └── errors_txt.log
├── launcher.py
└── run_pipeline.bat
```

---

## ⚙️ Como Executar
Exemplo com saídas padrão:
```bash
python scripts/weather_pipeline.py --file_content ENTRADA/cidades.txt --json --txt
```

Saídas personalizadas:
```bash
python scripts/weather_pipeline.py --file_content ENTRADA/cidades.txt --file_csv clima.csv --file_json clima.json --txt
```

Opções de logging:
- `--log_json` → logs estruturados em JSON  
- `--log_txt` → logs em texto simples (default)  

---

## 📊 Exemplo de Saída

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

---

## 🧠 Funções Internas (para desenvolvedores)
- `request_api()` → Faz requisições à API com retries  
- `extract_data()` → Extrai campos relevantes da resposta da API  
- `generate_report()` → Cria relatórios em JSON/TXT  
- `save_results()` → Move resultados e logs para a pasta `result/`  
- `main()` → Controla o pipeline de execução  

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
- **Sobrescrita de dados**: CSV e JSON são sobrescritos a cada execução. Se precisar de versionamento, adicione timestamps aos nomes.  
- **Limites da API**: a OpenWeather possui limites de requisição; para grandes lotes, considere adicionar delays.  
- **Encoding**: UTF-8 é usado para relatórios e saídas.  
- **Exit codes**: atualmente não diferenciados. Adicionar `sys.exit(0/1)` melhora integração com CI/CD.  
---