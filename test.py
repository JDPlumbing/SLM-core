from openai import OpenAI
import os
from dotenv import load_dotenv  # ✅ this line

load_dotenv()  # ✅ loads your .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

models = [m.id for m in client.models.list().data]
print("✅ gpt-4o access available!" if "gpt-4o" in models else "❌ gpt-4o not accessible")
