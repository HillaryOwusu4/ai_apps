# AI Toolkit API

A Django REST API powered by Anthropic's Claude — four AI endpoints for generation, analysis, and document Q&A.

## Features

📄 **DocChat (RAG)** ⭐ — Ask questions about any document using semantic search
🍳 **Recipe Generator** — Send ingredients, get a structured recipe
📊 **Review Analyzer** — Sentiment, issues & suggested replies
📧 **Subject Line Generator** — Email subject lines in any tone

## 🤖 Document Agent (RAG + Tool Use)

An AI agent that decides WHEN to search a document, rather than always 
retrieving. Combines semantic RAG with Claude's tool-use loop.

**Architecture:**
- `search_document` (semantic RAG) is exposed to Claude as a TOOL
- Claude autonomously decides whether to call it based on the question
- The agent loop runs: think → call tool → observe result → answer
- Search uses sentence-transformer embeddings + cosine similarity

**Why it matters:** Unlike plain RAG (which always retrieves), the agent 
reasons about when retrieval is needed — closer to how production AI assistants work.
## ⭐ Flagship: DocChat — RAG Document Q&A

Ask questions about any document. Uses semantic search with
sentence-transformer embeddings — finds answers by MEANING,
not keywords ("how do I get my money back?" correctly matches
"refund policy" with zero shared words).

**How it works:**
1. Document is chunked into passages
2. Each chunk + the question are embedded (all-MiniLM-L6-v2)
3. Cosine similarity ranks chunks by relevance
4. Top chunks are passed to Claude with strict grounding instructions
5. Claude answers ONLY from the document — no hallucination

## Tech Stack
- Python 3.12
- Django + Django REST Framework
- Anthropic Claude API
- sentence-transformers (local embeddings)
- python-dotenv

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/docchat/ | Ask questions about a document (RAG) |
| POST | /api/recipes/generate/ | Generate a recipe from ingredients |
| POST | /api/customer_review/analyze/ | Analyze a customer review |
| POST | /api/emails/email_subject/ | Generate email subject lines |

## Setup
```bash
git clone https://github.com/HillaryOwusu4/ai_apps
cd ai_apps
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
# Add your ANTHROPIC_API_KEY to a .env file
python manage.py migrate
python manage.py runserver
```

## Example

**Request:** `POST /api/docchat/`
```json
{ "document": "Refunds are accepted within 30 days. Shipping takes 5 days.", "question": "How do I get my money back?" }
```
**Response:**
```json
{ "question": "How do I get my money back?", "answer": "Refunds are accepted within 30 days." }
```

---
Built by Hillary Ameyaw Owusu