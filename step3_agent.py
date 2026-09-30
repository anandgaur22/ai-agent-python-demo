"""
STEP 3 - The complete AI Agent

AGENT = LLM (brain) + TOOLS (hands) + LOOP (think -> act -> observe -> think again)

The loop:
  1. Send the messages + tools to the model
  2. If the model asks for a tool -> run it -> add the result to messages -> go to step 1
  3. If the model does not ask for a tool -> that is the final answer
"""
import json
from config import client, MODEL
from tools import TOOLS, FUNCTIONS

SYSTEM_PROMPT = (
    "You are a helpful AI assistant. Use the given tools for live data, "
    "calculations, the current time, or saving notes. Keep answers short and clear."
)
MAX_STEPS = 6   # Safety limit to avoid an infinite loop


def run_agent(user_msg, history):
    history.append({"role": "user", "content": user_msg})

    for step in range(1, MAX_STEPS + 1):
        response = client.chat.completions.create(
            model=MODEL, messages=history, tools=TOOLS
        )
        msg = response.choices[0].message

        # No tool needed -> this is the final answer
        if not msg.tool_calls:
            history.append({"role": "assistant", "content": msg.content})
            return msg.content

        # Save the model's tool request in the history
        history.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [tc.model_dump() for tc in msg.tool_calls],
        })

        # Run every requested tool and send the result back
        for tc in msg.tool_calls:
            name = tc.function.name
            args = json.loads(tc.function.arguments or "{}")
            print(f"   [Step {step}] Tool: {name}({args})")
            try:
                result = FUNCTIONS[name](**args)
            except Exception as e:
                result = f"Tool error: {e}"
            print(f"   [Step {step}] Result: {result}")
            history.append({"role": "tool", "tool_call_id": tc.id, "content": str(result)})

    return "Reached the maximum number of steps without a final answer."


if __name__ == "__main__":
    history = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("AI Agent is ready! (type 'exit' to quit)\n")
    print("Try these:")
    print("  - What is the weather in Delhi?")
    print("  - What is the temperature difference between Delhi and Mumbai?")
    print("  - What time is it? Save it as a note.\n")

    while True:
        q = input("You: ").strip()
        if q.lower() in ("exit", "quit"):
            break
        if not q:
            continue
        print("Agent:", run_agent(q, history), "\n")
