import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from groq_setup import ChatGroqWrapper
from weather_functions import get_weather

current_weather = get_weather('goa')
system_prompt = 'You are an helpful assistant you answer only based on the given data in the prompt'

chat = ChatGroqWrapper(
    system_prompt=system_prompt,
    temperature=1,
    max_completion_tokens=8192,
    top_p=1,
    reasoning_effort="medium"
)

user_query = f"""
Should I pack a winter jacket for my trip to Goa, considering the current weather conditions? 
The current temperature is {current_weather}.
"""
response = chat.invoke(user_query, stream=True)

for chunk in response:
    print(chunk.choices[0].delta.content or "", end="")