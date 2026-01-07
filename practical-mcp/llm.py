import google.generativeai as genai
import os 

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def call_llm(context):
    response = model.generate_content(context)
    return response.text