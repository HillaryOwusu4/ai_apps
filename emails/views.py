from django.shortcuts import render
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import anthropic
import os
from dotenv import load_dotenv
import json
load_dotenv()
# Create your views here.
@api_view(['POST'])
def email_subject_generator(request):
    email_body = request.data.get('email_body')
    tone = request.data.get('tone','Let claude decide the tone based on the email body')
    client =  anthropic.Anthropic(api_key= os.environ.get("ANTHROPIC_API_KEY"))
    if not email_body:
        return Response(
            {"error": "Please provide email body"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    prompt = f"""
  
You are a helpful assistant for generating email subjects. The user has this email body: {email_body}
Please generate a concise, catchy subject line for this email. nd respond with a JSON object in this exact format, no other text:,
{{
"subject_options":["3" ,"subject", "line", "options"],
"tone":{tone},
"recommended_pick":"the best subject line from the options"
}}
"""
    message = client.messages.create(
    model='claude-sonnet-4-5-20250929', 
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}])

    response_text = message.content[0].text
    clean_text = response_text.replace("```json", "").replace("```", "").strip()
    generated_subject = json.loads(clean_text)
    return Response(generated_subject, status=200)