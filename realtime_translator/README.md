**📘 Real-Time Translator

A lightweight real-time multilingual translation and support interface, powered by FastAPI and local HuggingFace MarianMT models — no API keys required.

This project automatically:

1. 🌍 Detects the input language
2. 🔁 Translates text → English using local AI models
3. 💬 Generates a canned support-style response
4. 🧪 Includes a mini UI, Docker support, CI workflow, and Postman collection

_________________________________________________________________
Features:

1. Local translation pipeline powered by Helsinki-NLP / MarianMT
2. Language detection via langdetect
3. FastAPI backend with clean /api/query endpoint
4. Static HTML UI for instant testing
5. Docker & Docker Compose support
6. GitHub Actions CI (pytest automation)
7. Postman collection for API testing
No external translation API or OpenAI key required.**

_________________________________________________________________
Project Structure:

realtime_translator/
├── .github/
│   └── workflows/
│       └── ci.yml
├── static/
│   └── index.html
├── tests/
│   └── test_basic.py
├── app.py
├── docker-compose.yml
├── Dockerfile
├── postman_collection.json
├── README.md
└── requirements.txt

_________________________________________________________________
## Execution instructions:
Run locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Open http://localhost:8000

_________________________________________________________________