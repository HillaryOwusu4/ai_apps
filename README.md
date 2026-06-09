# AI Toolkit API

A Django REST API powered by Anthropic's Claude, offering three AI-powered endpoints for content generation and analysis.

## Features

🍳 **Recipe Generator** — Send ingredients, get a structured recipe
📊 **Review Analyzer** — Analyze customer reviews for sentiment, issues & suggested replies
📧 **Subject Line Generator** — Generate email subject lines in any tone

## Tech Stack

- Python 3.12
- Django + Django REST Framework
- Anthropic Claude API
- python-dotenv

## Endpoints

| Method | Endpoint                | Description                        |
| ------ | ----------------------- | ---------------------------------- |
| POST   | /api/recipes/generate/  | Generate a recipe from ingredients |
| POST   | /api/customer_review/analyze/   | Analyze a customer review          |
| POST   | /api/emails/email_subject/ | Generate email subject lines       |

## Setup

\`\`\`bash
git clone https://github.com/HillaryOwusu4/ai-toolkit-api
cd ai-toolkit-api
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt

# Add your ANTHROPIC_API_KEY to a .env file

python manage.py migrate
python manage.py runserver
\`\`\`

## Example

**Request:** \`POST /api/emails/email_subject/\`
\`\`\`json
{ "email_body": "Q3 numbers are in, we beat targets by 20%", "tone": "exciting" }
\`\`\`
**Response:**
\`\`\`json
{ "subject_options": ["🎉 Q3 Results: We Crushed Our Targets by 20%!", ...], "recommended_pick": "..." }
\`\`\`

---

Built by Hillary Ameyaw Owusu
