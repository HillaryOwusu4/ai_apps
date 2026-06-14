import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# The REAL function (the hands)
def calculator(expression):
    return str(eval(expression))   # eval("2+3*4") → 14

# The tool description (the menu Claude reads)
tools = [
    {
        "name": "calculator",
        "description": "Performs exact math calculations. Use this for ANY arithmetic instead of doing it yourself.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "A math expression like '2+3*4'"}
            },
            "required": ["expression"]
        }
    }
]
messages = [{"role": "user", "content": "What is (847 * 392) + (156 * 23)? Calculate each part separately."}]

max_steps = 5   # safety limit — never loop forever
step = 0

while step < max_steps:
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

    if response.stop_reason == "tool_use":
        # Claude may request SEVERAL tools at once — handle them ALL
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = calculator(block.input["expression"])
                print(f"Step {step + 1}: calculator({block.input['expression']}) = {result}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})   # ALL results together
        step += 1
    else:
        # No tool requested — Claude gave its final answer
        print("FINAL:", response.content[0].text)
        break