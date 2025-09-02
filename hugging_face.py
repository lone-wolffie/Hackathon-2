import requests
import os

HF_API_KEY = os.getenv("HF_API_KEY") 

def enrich_ingredients(raw_input):
    url = "https://api-inference.huggingface.co/models/google/flan-t5-base"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": f"Rephrase this for recipe search: {raw_input}"}

    
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json()[0]["generated_text"]
    except Exception as e:
        print("Hugging Face error:", e)
        return raw_input  # fallback if model fails





