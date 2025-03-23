import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Use the OpenAI client
client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)

