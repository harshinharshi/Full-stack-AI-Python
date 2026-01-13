# import sys
# from pathlib import Path

# # Add parent directory to Python path
# sys.path.insert(0, str(Path(__file__).parent.parent))

from groq_setup import ChatGroqWrapper

system_prompt = '''You are a math expert. Respond only to math-related queries.'''

chat = ChatGroqWrapper(
    system_prompt=system_prompt,
    temperature=1,
    max_completion_tokens=8192,
    top_p=1,
    reasoning_effort="medium"
)

user_query = input("User: ")
response = chat.invoke(user_query, stream=True)

for chunk in response:
    print(chunk.choices[0].delta.content or "", end="")