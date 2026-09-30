"""
STEP 2 - Show the tools to the model

Lesson: The model does NOT run the tool itself. It only says
"I need get_weather(city='Delhi')". Our code runs the tool.
"""
import json
from config import client, MODEL
from tools import TOOLS, FUNCTIONS

question = "What is the temperature in Delhi right now?"
print("You:", question)

response = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": question}],
    tools=TOOLS,
)
msg = response.choices[0].message

if msg.tool_calls:
    for tc in msg.tool_calls:
        args = json.loads(tc.function.arguments or "{}")
        print(f"\n>> The model asked for a tool: {tc.function.name}({args})")
        result = FUNCTIONS[tc.function.name](**args)
        print(f">> Our code ran the tool. Result: {result}")
    print("\n>> Next, this result must go back to the model, and we must repeat this")
    print(">> until the model gives a final answer. That is the AGENT LOOP -> step3_agent.py")
else:
    print("The model did not ask for a tool:", msg.content)
