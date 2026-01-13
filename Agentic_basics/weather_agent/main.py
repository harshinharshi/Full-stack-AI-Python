from groq_setup import ChatGroqWrapper
from weather_functions import get_weather

system_prompt = '''You are a weather expert. Respond only to weather-related queries. 
You have access to a function called `get_weather(city)` that retrieves the weather for a given city. 
The function accepts a single input: the city name (e.g., `get_weather("Goa")`) and returns the current weather for that city.
'''

available_functions = {
    "get_weather": get_weather
}

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