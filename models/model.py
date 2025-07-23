from gpt4all import GPT4All
import os

MODEL_PATH = os.path.join("models", "gpt4all-model.bin")
model = GPT4All(model_name=MODEL_PATH, allow_download=False)

def generate_response(prompt):
    response = model.generate(prompt, max_tokens=200)
    return response.strip()