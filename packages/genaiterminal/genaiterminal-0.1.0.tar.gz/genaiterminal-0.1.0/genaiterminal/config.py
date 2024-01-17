import google.generativeai as genai

def configure_api_key(api_key):
    genai.configure(api_key=api_key)

