
# import openpyxl
import time
import requests
import json
import os

from consts import MAX_TOKENS, TEMPERATURE

#### Grok 3 ####

from openai import OpenAI

def generate_Grok3(prompt, system_message=""):
    message = []
    if system_message:
        message.append({"role": "system", "content": system_message})
    message.append({"role": "user", "content": prompt})
    while True:
        try:
            client = OpenAI(
                api_key="API_KEY",
                base_url="https://api.x.ai/v1"
            )

            response = client.chat.completions.create(
                messages=message,
                model="grok-3",
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                logprobs=True,
            )
            message_content = response.choices[0].message.content
            return message_content, response
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(1.0)
            continue

if __name__ == "__main__":
    x = generate_Grok3('hi',)
    print(x)