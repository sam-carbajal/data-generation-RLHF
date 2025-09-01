from streamlit import st
from google import genai
from openai import OpenAI

class StoryGenerator:
    def __init__(self, model: str, client_key):
        self.model = model
        self.client_key = client_key

    def generate(self, prompt: str):
        response = self.client_key.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text.strip()

def ClientKey(model):
    if model == "gemini-2.5-flash" or model == "gemini-2.5-pro":
        return genai.Client(api_key=st.secrets['OPENAI_API_KEY'])
    elif model == "gpt-4o-mini" or model == "gpt-4o":
        return OpenAI(
                api_key=st.secrets['GEMINI_API_KEY']
            )
    #elif model == "deepseek-chat":
    #    return api_key
    else:
        raise ValueError(f"Unknown model: {model}")
    

def GenerateResponse(client_key, model, prompt):
    if model == "gemini-2.5-flash" or model == "gemini-2.5-pro":
        response = client_key.models.generate_content(
            model=model, contents=prompt
        )
        return response.text.strip()
    elif model == "gpt-4o-mini" or model == "gpt-4o":
        response = client_key.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

