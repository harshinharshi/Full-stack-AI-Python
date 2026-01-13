import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from groq_setup import ChatGroqWrapper
from weather_functions import get_weather

current_weather = get_weather('goa')
system_prompt = '''
you run in a loop of thought, action, pause, action_response.
At end of the loo you output an answer.

Use Thought to understand teh question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Action_Response will be the result of ranking those actions

Your available actions are :

get_weather
eg: get_weather(mumbai)
returns the current temperature in the city

Example session:

Question : Should I take an winter jacket with me today in Mumbai?
Thought : I should check the weather in mumbai first.
Action : get_weather(Mumbai)
PAUSE

you will be called again with this:

Action_Response: 1 degree celsius in mumbai

You then output:
Answer : yes there is 1 degree celsius in mumbai so a winter jacket is needed
'''
chat = ChatGroqWrapper(
    system_prompt=system_prompt,
    temperature=1,
    max_completion_tokens=8192,
    top_p=1,
    reasoning_effort="medium"
)

user_query = f"""
Should I pack a winter jacket for my trip to Goa.
"""
response = chat.invoke(user_query)

print(response.choices[0].message.content)
