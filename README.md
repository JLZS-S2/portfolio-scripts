# Portfolio Scripts – Automações Python Prontas para Produção

## 🎯 O que você encontra aqui
Sou João, dev Python focado em automação que economiza horas de trabalho manual.  
Este repositório reúne **7 pipelines prontos**, testados e documentados, para **organizar arquivos**, **integrar APIs** e **tratar dados CSV/JSON/PDF/TXT**.  
Todos com `.bat` executável: o cliente só clica e roda. Zero terminal.  
👉 E, se preferir, posso entregar cada projeto também em **formato `.exe`**, para rodar sem precisar instalar Python.

---

## 📦 Projetos Disponíveis | Available Projects
### 1. CSV to SQLite
**O que faz:** Converte `.csv` em banco `.sqlite` automaticamente. Remove duplicatas, trata nulos, gera relatório `.txt` ou `.json`.  
**Benefício:** Em segundos, você tem um banco pronto para análise.  
**Docs:** [/csv_to_sqlite/README.md](/csv_to_sqlite/README.md)
**Downloads:** [⬇️ CSV_TO_SQLITE_v1.0.zip](https://github.com/JLZS-S2/portfolio-scripts/releases/download/csv_to_sqlite_v1.0/CSV_TO_SQLITE_v1.0.zip)

### 2. PDF to CSV
**O que faz:** Extrai tabelas e texto de PDFs direto para `.csv` limpo.  
**Benefício:** Elimina copiar e colar manual de relatórios.  
**Docs:** [/pdf_to_csv/README.md](/pdf_to_csv/README.md) 
**Downloads:** [⬇️ PDF_TO_CSV_V1.0.zip](https://github.com/JLZS-S2/portfolio-scripts/releases/download/pdf_to_csv_v1.0/PDF_TO_CSV_v1.0.zip)

### 3. JSON to CSV
**O que faz:** Valida, concatena e converte múltiplos `.json` em `.csv` único.  
**Benefício:** Junta respostas de API em planilha sem abrir código.  
**Docs:** [/json_to_csv/README.md](/json_to_csv/README.md)
**Downloads:** [⬇️ JSON_TO_CSV_V1.0.zip](https://github.com/JLZS-S2/portfolio-scripts/releases/download/json_to_csv_v1.0/JSON_TO_CSV_v1.0.zip)

### 4. File Organizer
**O que faz:** Organiza arquivos por extensão em subpastas, move ou copia conforme configuração, gera relatórios e compacta resultados em `.zip`.  
**Benefício:** Estrutura automaticamente pastas bagunçadas, com contagem de arquivos e logs para auditoria.  
**Docs:** [/file_automation/README.md](/file_automation/README.md)
**Downloads:** [⬇️ FILE_ORGANIZER_V1.0.zip](https://github.com/JLZS-S2/portfolio-scripts/releases/download/file_automation_v1.0/FILE_ORGANIZER_v1.0.zip)

### 5. Merge & Filter CSV
**O que faz:** Junta múltiplos `.csv`, remove duplicados e aplica filtros dinâmicos via `filter.json`.  
**Benefício:** Cria datasets filtrados sem precisar abrir Excel.  
**Docs:** [/merge_filter_csv/README.md](/merge_filter_csv/README.md)
**Downloads:** [⬇️ MERGE_&_FILTER_CSV_V1.0.zip](https://github.com/JLZS-S2/portfolio-scripts/releases/download/merge_filter_csv_v1.0/MERGE_FILTER_CSV_v1.0.zip)

### 6. Text Processing
**O que faz:** Limpa `.txt`, remove linhas em branco, divide por palavras-chave e conta linhas/palavras.  
**Benefício:** Processa relatórios textuais em segundos.  
**Docs:** [/text_processing/README.md](/text_processing/README.md)
**Downloads:** [⬇️ TEXT_PROCESSING_V1.0.zip](https://github.com/JLZS-S2/portfolio-scripts/releases/download/text_processing_v1.0/TEXT_PROCESSING_v1.0.zip)

### 7. Weather Data
**O que faz:** Integra com API OpenWeather, coleta dados de cidades e exporta para `.csv` e `.json`.  
**Benefício:** Relatórios meteorológicos prontos para análise.  
**Docs:** [/weather_pipeline/README.md](/weather_pipeline/README.md)
**Downloads:** [⬇️ WEATHER DATA V1.0.zip](https://github.com/JLZS-S2/portfolio-scripts/releases/download/weather_pipeline_v1.0/WEATHER_PIPELINE_v1.0.zip)

*Cada pasta tem `run_pipeline.bat`, `launcher.py`, `LEIAME.txt` e `requirements.txt`. É baixar e rodar.  
E, sob demanda, posso entregar cada projeto como `.exe` para máxima praticidade.*

---

## ⚙️ Como usar | How to Use

**Para clientes | For clients:**
1. Baixe o `.zip` do projeto desejado (seção acima)  
2. Extraia, coloque seus arquivos na pasta `ENTRADA/`  
3. Clique 2x em `run_pipeline.bat` ou no `.exe` fornecido  
4. Resultado sai na pasta `result/`  

**Para desenvolvedores | For developers:**
```bash
git clone https://github.com/JLZS-S2/portfolio-scripts.git
cd portfolio-scripts/csv_to_sqlite
pip install -r requirements.txt
python scripts/csv_to_sqlite.py --input dados.csv --txt
```

---

## 🖥️ Versão `.exe` | Executável Standalone
Para clientes que não querem instalar Python ou lidar com dependências, cada pipeline pode ser entregue também em **formato `.exe`**:
- Basta clicar duas vezes no arquivo `.exe` para rodar.  
- Funciona em qualquer Windows moderno.  
- Inclui todas as dependências embutidas.  
- Ideal para uso corporativo ou clientes finais sem conhecimento técnico.  

---

## 📬 Contato Comercial | Business Contact
Precisa de customização ou automação sob demanda?  
- Email: joaolzss604@gmail.com  


---

## 📜 Licença | License
MIT License. Uso comercial permitido com atribuição.  
Commercial use allowed with attribution.

---
