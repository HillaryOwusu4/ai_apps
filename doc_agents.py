import anthropic
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util
load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

model = SentenceTransformer('all-MiniLM-L6-v2')

def search_document(query,document):
    chunk = document.lower().split('\n')

    filtered_chunk = [c for c in chunk if c.strip()]

    question = model.encode(query)
    print(question)

    scored_chunk = []
    for c in filtered_chunk:
        embeded_chunk = model.encode(c)
        overlap = util.cos_sim(question,embeded_chunk).item()
        scored_chunk.append((overlap, c))
    
    scored_chunk.sort(reverse=True)
    top_chunks = [c for score, c in  scored_chunk[:3]]
    relevant_text = '\n'.join(top_chunks)
    return relevant_text

document = "Refunds are accepted within 30 days.\nShipping takes 5 business days.\nWe are located in Accra."
messages = [{"role": "user", "content": "How do I get my money back?"}]
tools = [
    {
        "name": "search_document",          # what's the tool called?
        "description": "Use this to search the document for relevant information when you need to answer a question about it.",   # what does it do? (Claude reads THIS to decide when to use it)
        "input_schema": {
            "type": "object",
            "properties": {
               "query": {"type": "string", "description": "A question from the user about the document"},
            },
            "required": ['query']
        }
    }
]
max_steps = 5
step = 0

while step < max_steps:
   response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )
   if response.stop_reason == "tool_use":
       tool_results = []
       for block in response.content:
           if block.type == 'tool_use':
               query = block.input['query']
               results = search_document(query,document)
               tool_results.append({
            "type": "tool_result",
            "tool_use_id": block.id,        # ← matches the request!
            "content": results
        })
       messages.append({"role":'assistant',"content":response.content})
       messages.append({"role":'user',"content":tool_results})
       step += 1
   else:
        # No tool requested — Claude gave its final answer
        print("FINAL:", response.content[0].text)
        break
           
      