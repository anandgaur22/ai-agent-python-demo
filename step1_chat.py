"""
STEP 1 - Just the LLM (this is NOT an agent yet)

Lesson: The model can only generate text. It has no real-time data
(today's weather, the current time) and it cannot take any action.
"""
from config import client, MODEL

question = "What is the temperature in Delhi right now?"
print("You:", question)

response = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": question}],
)

print("LLM:", response.choices[0].message.content)
print("\n>> Notice: the model has no live data. It will either refuse or guess.")
print(">> To fix this, we must give the model TOOLS -> step2_tools.py")
