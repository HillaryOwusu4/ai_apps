from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import anthropic
import os
from dotenv import load_dotenv
import json
load_dotenv()
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')
# Create your views here.
@api_view(['POST'])
def doc_chat(request):
    document = request.data.get('document')
    question = request.data.get('question')
    client =  anthropic.Anthropic(api_key= os.environ.get("ANTHROPIC_API_KEY"))
    if not document or not question:
        return Response(
            {"error": "Please provide both document and question"},
            status=status.HTTP_400_BAD_REQUEST
        )
    chunk = document.lower().split('\n') 

    filtered_chunk = [c for c in chunk if c.strip() ]

    question_word = model.encode(question)

    scored_chunk = []

    for k in filtered_chunk:
        chunk_word = model.encode(k)
        overlap = util.cos_sim(question_word, chunk_word).item()
        scored_chunk.append((overlap, k))

    scored_chunk.sort(reverse=True)
    top_chunks = [chunk for score, chunk in scored_chunk[:3]]
    print("CHUNKS:", chunk)              # should be a list of strings
    print("SCORED:", scored_chunk)
    relevant_text = "\n".join(top_chunks)
    prompt = f""" You are a document assistant , {relevant_text} is the handful of chunks from the document that best match the user's question.Answer, using ONLY the document above ,If the answer isn't in it, say you couldn't find itand respond with a JSON object in this exact format, no other text: {{
    "question":{question},
    "answer":"add your response here"
    
    }}
"""
    message = client.messages.create(
    model='claude-sonnet-4-5-20250929', 
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}])
            # should be list of (number, string)
    response_text = message.content[0].text
    clean_text = response_text.replace("```json", "").replace("```", "").strip()
    generated_subject = json.loads(clean_text)
    return Response(generated_subject, status=200)