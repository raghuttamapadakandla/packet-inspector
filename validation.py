from dotenv import load_dotenv
import os
import requests
import json
from flask import Flask, request
import re

load_dotenv()
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')

def callGPT(request):
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer "+OPENROUTER_API_KEY,
        "Content-Type": "application/json",
    },
    data=json.dumps({
        "model": "deepseek/deepseek-r1:free",
        "messages": [
        {
            "role": "user",
            "content": "ip = "+str(request.headers.get('X-Forwarded-For'))+" headers = "+str(request.headers)+" body = "+str(request.json) + " On a scale of 1 to 10, rate how malicious this data packet seems. With 1 being the least likely and 10 being the most likely. At the end of the answer return the final answer in this format - rating: <Final Rating Calculated between 1 and 10>"
        }
        ],
        
    })
    )
    rating, reasoning = extract_rating_and_reasoning(response)
    return rating, reasoning

def extract_rating_and_reasoning(response):
    response = response.json()
    content = response['choices'][0]['message']['content']

    # Regex to capture 'rating: <number>' and the reasoning part
    rating_match = re.search(r'rating\s*:\s*(\d+)', content, re.IGNORECASE)
    reasoning = response['choices'][0]['message'].get('reasoning', 'None')

    rating = rating_match.group(1) if rating_match else 'None'

    print(f"Rating: {rating}")
    print(f"Reasoning: {reasoning}")
    return rating, reasoning