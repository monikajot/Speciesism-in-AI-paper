import os
import time

import openai
from openai import OpenAI
from json.decoder import JSONDecodeError
import json
from typing import Optional
import anthropic
import google.generativeai as genai
from google.api_core import exceptions
from llama_api import  generate_Llama
from grok_api import generate_Grok3
from deepseek_api import generate_DeepSeekR1
from consts import MAX_TOKENS, TEMPERATURE

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


llama_client = OpenAI(
    api_key = "API-KEY",
    base_url = "https://api.llama-api.com"
)
llama_client_small = OpenAI(
    api_key = "API-KEY",
    base_url = "https://api.llama-api.com"
)
CLAUDE_API = os.environ.get("ANTHROPIC_API_KEY")
# claude = anthropic.Anthropic(api_key=CLAUDE_API)

api_key = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
TEMPERATURE =1
def query_model(model, message, system, logprobs=True, temp=1):
    response = None
    completion = None
    try:


        if model == "gpt-3.5":
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": message},
                ],
                logprobs=logprobs, #temp default 1
            )

            # print(completion.choices[0].message)
            response = completion.choices[0].message.content
        if model == "gpt-4":
            completion = client.chat.completions.create(
                model="gpt-4-0613",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": message},
                ],
                logprobs=logprobs,
            )
            print(response)
            response = completion.choices[0].message.content
        if model == "gpt-5":
            completion = client.chat.completions.create(
                model="gpt-5",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": message},
                ],
                logprobs=logprobs,
            )
            # print(response)
            response = completion.choices[0].message.content

        if model == "gpt-4o-mini":
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": message},
                ],
                logprobs=logprobs,
            )
            response = completion.choices[0].message.content

        if model == "gpt-4o":
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": message},
                ],
                logprobs=logprobs,
            )
            # print(response)
            response = completion.choices[0].message.content
        if model == "gpt-4.1":
            completion = client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": message},
                ],
                logprobs=logprobs,

            )
            response = completion.choices[0].message.content
        if model == "o1":
            completion = client.chat.completions.create(
                model="o1",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": message},
                ],
                # logprobs=logprobs,

            )
            response = completion.choices[0].message.content
        if model == "o3-mini":
            completion = client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": message},
                ],
                # logprobs=logprobs,

            )
            response = completion.choices[0].message.content
        if model == "claude-2":
            # message = message
            completion = claude.messages.create(
                model="claude-2.1",
                max_tokens=1024,
                system=system,
                messages=[{"role": "user", "content": message}],
                temperature=TEMPERATURE,
            )
            response = completion.content[0].text
            # print(response)

        if model == "claude-3.5":
            # message = message
            completion = claude.messages.create(
                model="claude-3-5-sonnet-latest",
                max_tokens=MAX_TOKENS,
                system=system,
                messages=[{"role": "user", "content": message}],
                temperature=TEMPERATURE,
                # logprobs=logprobs,
            )
            # print(response)

            response = completion.content[0].text

        if model == "claude-3.7":
            # message = message
            completion = claude.messages.create(
                model="claude-3-7-sonnet-latest",
                max_tokens=MAX_TOKENS,
                system=system,
                messages=[{"role": "user", "content": message}],
                temperature=TEMPERATURE,
                # logprobs=logprobs,
            )
            response = completion.content[0].text
            # print(response)
        if model == "claude-4":
            # message = message
            completion = claude.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=MAX_TOKENS,
                system=system,
                messages=[{"role": "user", "content": message}],
                temperature=TEMPERATURE,
                # logprobs=logprobs,
            )
            response = completion.content[0].text

        if "llama" in model:
            response, completion = generate_Llama(prompt=message, model=model, system_message=system)

        if model == "gemini-1.5":
            model = genai.GenerativeModel("gemini-1.5-flash")
            response_text = model.generate_content(message)
            try:
                response = response_text.text
            except ValueError:
                pass

        if model == "gemini-2":
            model = genai.GenerativeModel("gemini-2.0-flash")
            response_text = model.generate_content(message)
            try:
                response = response_text.text
            except ValueError:
                pass

        if model == "gemini-2.5":
            model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
            response_text = model.generate_content(message)
            try:
                response = response_text.text
            except ValueError:
                pass
        if model == "grok":
            response, completion = generate_Grok3(prompt=message, system_message=system)
        if model == "deepseek-r1" or model == "deepseek-v3":
            response, completion = generate_DeepSeekR1(prompt=message, system_message=system, model=model)

    except (ValueError, anthropic.InternalServerError, openai.BadRequestError, exceptions.ResourceExhausted):
        time.sleep(30)
        response, completion = query_model(model, message, system)
    return response, completion


def string_to_json(text) -> Optional[dict]:
    try:
        example_dict = json.loads(text)
    except JSONDecodeError:
        response, _ = query_model(
            "claude-3.5",
            f"Can you format the following string to be in JSON format? If there's any additional text around the JSON dictionary, just skip it. The output must be ONLY reformatted JSON readable python string with \"answer\"  and \"justification\" as keys. If I run python function json.loads(), it must work on your raw output. TEXT: {text}",
            "",
        )
        # print(response)
        try:
            example_dict = json.loads(response)
        except JSONDecodeError:
            return
    return example_dict


if __name__ == "__main__":
    from openai import OpenAI

    client = OpenAI()

    resp = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": "Translate to French: Hello, how are you?"}],
        logprobs=True,
        top_logprobs=3,    )





