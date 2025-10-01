#### DeepSeek-R1 ####
import re
import requests
import json
import time
from consts import TEMPERATURE, MAX_TOKENS, TOP_K, TOP_P

DS_MODELS = {"deepseek-r1": "accounts/fireworks/models/deepseek-r1", "deepseek-v3": "accounts/fireworks/models/deepseek-v3"}
def generate_DeepSeekR1(prompt, system_message, model):
    model_ = DS_MODELS[model]
    message = []
    # if system_message:
    message.append({"role": "system", "content": "Always respond with only the final output, never including any <think/> or thinking sections."})
    message.append({"role": "user", "content": prompt})
    i=0
    while True:
        try:
            url = "https://api.fireworks.ai/inference/v1/chat/completions"
            payload = {
              "model": model_,
              "max_tokens": MAX_TOKENS,
              "top_p": TOP_P,
              "top_k": TOP_K,
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

            json_pattern = re.compile(r'</think>\s*(.*)', re.DOTALL)
            match = json_pattern.search(response_json["choices"][0]["message"]["content"])

            if match:
                json_string = match.group(1).strip()
            return json_string, response_json
        except Exception as e:
            return 1,1


if __name__ == "__main__":
    response, json_ = generate_DeepSeekR1("hi", "", "deepseek-r1")
    print(response)
    a=1