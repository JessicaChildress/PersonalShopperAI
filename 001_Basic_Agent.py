"""
Owner: Jessica Childress
Description: This file will be used to create an AI agent using a connection to Open AI. 
Sources: 
    https://youtu.be/bZzyPscbtI8?si=Z5Ih_38aoyp__Y6E (Building AI Agents in Pure Python)
    https://www.anthropic.com/research/building-effective-agents (Building Effective Agents)
"""
from openai import OpenAI
from dir_secrets import OPENAI_API_KEY

client = OpenAI(
    api_key=OPENAI_API_KEY
)

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful personal shopper."},
        {
            "role": "user",
            "content": "Help me find a dress to wear to my sister's wedding in June.",
        },
    ],
)

response = completion.choices[0].message.content
print(response)