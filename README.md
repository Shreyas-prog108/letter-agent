# Letter Agent

Letter Agent is an AI-powered document and employee data processing tool. It ingests HR policy PDFs and employee lists, stores them in a vector database, and enables advanced search and retrieval using language models.

## Features
- Ingests PDF documents and CSV employee lists
- Splits documents into semantic chunks
- Stores embeddings in a persistent Chroma vector database
- Uses OpenAI for embeddings (requires API key)
- Modular pipeline for easy extension

## Project Structure
```
letter-agent/
├── app.py
├── requirements.txt
├── .env
├── .gitignore
├── data/
│   ├── Employee_List.csv
│   ├── HR Leave Policy.pdf
│   ├── HR Offer Letter.pdf
│   └── HR Travel Policy.pdf
├── db/
│   └── chromadb/
└── src/
    ├── agent/
    │   ├── __init__.py
    │   ├── core.py
    │   ├── prompt.py
    │   └── tools.py
    └── pipeline/
        ├── __init__.py
        └── ingest.py
```

## Setup
1. **Clone the repository**
   ```sh
   git clone https://github.com/Shreyas-prog108/letter-agent.git
   cd letter-agent
   ```
2. **Create and activate a virtual environment**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set your OpenAI API key**
   - Create a `.env` file in the root directory:
     ```
     OPENAI_API_KEY=your-openai-api-key
     ```
5. **Add your data**
   - Place PDF and CSV files in the `data/` directory.

## Usage
To ingest data and create the vector store:
```sh
python src/pipeline/ingest.py
```

## Notes
- The `db/` directory and `.env` file are excluded from version control via `.gitignore`.
- Requires Python 3.12+ and an OpenAI API key.

## License
MIT
