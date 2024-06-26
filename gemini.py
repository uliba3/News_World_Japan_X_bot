# Import the Python SDK
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
# Used to securely store your API key
import os
from dotenv import load_dotenv
import time
from queue import Queue

# Load environment variables from .env file
load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

modelFlash = genai.GenerativeModel('gemini-1.5-flash')
modelPro = genai.GenerativeModel('gemini-1.5-pro')
q = Queue(maxsize = 15)

def runModel(model, prompt):
    if model == "flash":
        model = modelFlash
    else:
        model = modelPro
    while q.full() and q.queue[0] > time.time() - 60:
        time.sleep(1)
    if q.full():
        q.get()
    response = model.generate_content(
        prompt,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        }
    )
    q.put(time.time())
    print(f"prompt: {prompt}\nresponse: {response.text}")
    return response.text

if __name__ == "__main__":
    runModel("flash", "Do you like me?")
