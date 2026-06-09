from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import anthropic
import os
import json
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


@api_view(['POST'])
def generate_recipe(request):
    # 1. Get ingredients from the request (sent by frontend/Thunder Client)
    ingredients = request.data.get('ingredients')

    # 2. Safety check — did they actually send ingredients?
    if not ingredients:
        return Response(
            {"error": "Please provide ingredients"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 3. Build the prompt (same one from your script)
    prompt = f"""You are a creative chef.

The user has these ingredients: {ingredients}

Create a simple recipe using these ingredients. Respond ONLY with valid JSON in this exact format, no other text:
{{
    "dish_name": "name of the dish",
    "cooking_time": "e.g. 30 minutes",
    "ingredients_needed": ["item 1", "item 2"],
    "steps": ["step 1", "step 2", "step 3"]
}}"""

    # 4. Call Claude (same as your script)
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    # 5. Clean and parse the response
    response_text = message.content[0].text
    clean_text = response_text.replace("```json", "").replace("```", "").strip()
    recipe = json.loads(clean_text)

    # 6. Send the recipe back to the frontend
    return Response(recipe, status=status.HTTP_200_OK)