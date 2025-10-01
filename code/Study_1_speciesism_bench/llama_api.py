import requests
import time
import json
from consts import TEMPERATURE, MAX_TOKENS, TOP_K, TOP_P


#### Llama 4 Maverick ####
Llama_model = {
    "llama4": "accounts/fireworks/models/llama4-maverick-instruct-basic",
    "llama3.1": "accounts/fireworks/models/llama-v3p1-405b-instruct",
    "llama3.3-70b": "accounts/fireworks/models/llama-v3p3-70b-instruct",
    "llama3.2-90b": "accounts/fireworks/models/llama-v3p2-90b-vision-instruct",
    "llama3.2-3b": "accounts/fireworks/models/llama-v3p2-3b",
}
def generate_Llama(prompt, model, system_message="", ):
    model_ = Llama_model[model]
    message = []
    if system_message:
        message.append({"role": "system", "content": system_message})
    message.append({"role": "user", "content": prompt})
    while True:
        try:
            url = "https://api.fireworks.ai/inference/v1/chat/completions"
            payload = {
              "model": model_,
              "max_tokens": 1000,
              "top_p": 1,
              "top_k": 40,
              "presence_penalty": 0,
              "frequency_penalty": 0,
              "temperature": TEMPERATURE,
              "logprobs": True,
              "messages": message}
            headers = {
              "Accept": "application/json",
              "Content-Type": "application/json",
              "Authorization": "AUTH_KEY"
            }
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
            response_json = response.json()
            return  response_json["choices"][0]["message"]["content"], response_json
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(1.0)
            continue

if __name__ == "__main__":
    x = generate_Llama('hi', model="llama3.3-70b")
    print(x)
    # a=1