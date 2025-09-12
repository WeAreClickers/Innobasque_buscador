import os
from dotenv import load_dotenv
import time
from openai import OpenAI
from utils import *

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

time_start = time.time()
text = "inteligencia artificial"
user_prompt = f"Tu tarea es interpretar el siguiente texto y ver si hay intencionalidad de filtrar alguno de los filtros:\n{text}"
with open('system_prompt.txt', 'r', encoding='utf-8') as f:
    system_prompt = f.read()
print(call_openai(client, user_prompt, system_prompt, max_tokens=256))
time_end = time.time()
time_elapsed = time_end - time_start

print(f"Tiempo de ejecución: {time_elapsed:.4f} segundos")