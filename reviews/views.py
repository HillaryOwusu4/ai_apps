from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import anthropic
import os
from dotenv import load_dotenv
import json
load_dotenv()
client = anthropic.Anthropic(api_key= os.environ.get("ANTHROPIC_API_KEY"))
@api_view(['POST'])
def customer_review(request):   
    review = request.data.get ('review')
    if not review:
        return Response(
            {"error": "Please provide review"},
            status=status.HTTP_400_BAD_REQUEST
        )
    prompt = f"""You are a helpful assistant for analyzing customer reviews. The user has this review: {review}
Please analyze the review and respond with a JSON object in this exact format, no other text:
{{
sentiment: "positive", "negative", or "neutral",
summary: "a brief summary of the review",
issues: ["list", "of", "any", "issues", "mentioned", "in", "the", "review"],
suggestions: ["list", "of", "any", "suggestions", "mentioned", "in", "the", "review"],
suggested_reply: "a polite, professional response addressing their complaint"
}}
"""
    message = client.messages.create(
    model='claude-sonnet-4-5-20250929',
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
  )
    response_text = message.content[0].text
    clean_text = response_text.replace("```json", "").replace("```", "").strip()
    review_analysis = json.loads(clean_text)

    return Response(review_analysis, status=200)
         
