import sys
from pathlib import Path
import json
import re

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from groq_setup import ChatGroqWrapper
from weather_functions import get_weather
from system_prompts import system_prompt


def llm_string_to_json(llm_output: str) -> dict:
    """
    Converts LLM string output to JSON.
    Algorithm: Regex extraction + json parsing
    """
    print("\n[Parser] Attempting to extract JSON from LLM output...")
    
    match = re.search(r"\{.*?\}", llm_output, re.DOTALL)
    if not match:
        raise ValueError("[Parser Error] No JSON found in LLM output")

    print("[Parser] JSON successfully extracted")
    return json.loads(match.group())


# ------------------ Tool Registry ------------------
available_actions = {
    "get_weather": get_weather
}

print("[Init] Available tools loaded:", list(available_actions.keys()))

# ------------------ LLM Initialization ------------------
chat = ChatGroqWrapper(
    system_prompt=system_prompt,
    temperature=1,
    max_completion_tokens=8192,
    top_p=1,
    reasoning_effort="medium"
)

print("[Init] ChatGroqWrapper initialized with system prompt")

# ------------------ Initial User Message ------------------
messages = [
    {"role": "user", "content": "Should I pack a winter jacket for my trip to Goa."}
]

print("\n[User] Initial question added to conversation")

# ------------------ Agent Loop ------------------
while True:
    print("\n================= NEW ITERATION =================")
    print("[Conversation State]")
    for msg in messages:
        print(f" → {msg['role'].upper()}: {msg['content']}")
    print("================================================")

    print("\n[LLM] Sending messages to the model...")
    response = chat.invoke(messages)

    assistant_reply = response.choices[0].message.content
    print("\n[LLM Response]")
    print(assistant_reply)

    # ------------------ Assistant Reply ------------------
    messages.append({
        "role": "assistant",
        "content": assistant_reply
    })

    # ------------------ Stop Condition ------------------
    if assistant_reply.strip().endswith("<stop>"):
        print("\n[Agent] <stop> detected — ending loop.")
        break

    # ------------------ Tool Request Detection ------------------
    if assistant_reply.strip().startswith("Thought"):
        print("\n[Agent] Thought detected — checking for tool request...")

        try:
            json_data = llm_string_to_json(assistant_reply)
        except Exception as e:
            print("[Agent Error]", e)
            break

        action_name = json_data.get("action")
        action_input = json_data.get("action_input")

        print(f"[Agent] Tool requested: {action_name}")
        print(f"[Agent] Tool input: {action_input}")

        if action_name in available_actions:
            print(f"[Tool] Executing '{action_name}'...")
            tool_fn = available_actions[action_name]
            tool_result = tool_fn(action_input)

            print(f"[Tool] Result received: {tool_result}")

            # ------------------ Observation (ReAct style) ------------------
            messages.append({
                "role": "assistant",
                "content": f"Observation: {tool_result}"
            })

            print("[Agent] Observation added back to conversation")
        else:
            print("[Agent Warning] Requested tool not available")

            messages.append({
                "role": "assistant",
                "content": "Observation: Requested tool not available"
            })
    else:
        print("[Agent] No tool request detected — exiting loop.")
        break


# ------------------ Final Conversation ------------------
print("\n================= FINAL CONVERSATION =================")
for msg in messages:
    print(f"{msg['role'].upper()}: {msg['content']}")
print("=====================================================")
