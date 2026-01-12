from groq_setup import ChatGroqWrapper

chat = ChatGroqWrapper(
    system_prompt="You are an expert in maths and only provide mathematical answers.",
    temperature=1,
    max_completion_tokens=8192,
    top_p=1,
    reasoning_effort="medium"
)
user_query = input("User: ")
response = chat.invoke(user_query, stream=True)

for chunk in response:
    print(chunk.choices[0].delta.content or "", end="")