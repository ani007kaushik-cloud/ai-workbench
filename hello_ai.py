import os
import sys
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, APIConnectionError

load_dotenv() #loads the environment variables from the .env file

api_key=os.getenv("OPENAI_API_KEY")

if not api_key:
    print("ERROR: OPENAI_API_KEY not found")
    print("COPY .env.example to .env and add your key.")
    sys.exit(1)

client= OpenAI(api_key=api_key) #setsup the OpenAI client with the API key from the environment variable

MODEL=os.getenv("OPENAI_MODEL","gpt-4.1-mini") # setsup the gpt-4.1-mini model as the default model if no model is specified in the environment variable

# Pricing per 1M tokens (USD) — verify against https://openai.com/api/pricing before relying on this for cost tracking at scale
PRICE_PER_1M_INPUT = 0.40
PRICE_PER_1M_OUTPUT = 1.60

#--call block--# 

print("Sending prompt: What is the generative AI?")

try:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Be concise and precise."},
            {"role": "user", "content": "What is generative AI in concise three bullet points?"}
        ],
        temperature=0.1,
        max_tokens=100
    )

    print(f"Response:{response.choices[0].message.content}")
    print(f"Token_Used:{response.usage.total_tokens}")

    total_cost = ((response.usage.prompt_tokens / 1_000_000) * PRICE_PER_1M_INPUT) + \
                 ((response.usage.completion_tokens / 1_000_000) * PRICE_PER_1M_OUTPUT)
    print(f"Cost: ${total_cost:.6f}")

except AuthenticationError:
    print("Error:Invalid API Key. Check your .env file")
except APIConnectionError:
    print("Error: Internet Error. Check your internet connection.")
except Exception as e:
    print(f"Unexpected error:{e}")