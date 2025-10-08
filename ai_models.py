import requests
import streamlit as st
import google.generativeai as genai
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
        #return genai.Client(api_key=st.secrets['OPENAI_API_KEY'])
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        return genai.GenerativeModel(model)
    elif model == "gpt-4o-mini" or model == "gpt-4o" or model == "gpt-5":
        return OpenAI(
                api_key=st.secrets['OPENAI_API_KEY']
            )
    elif model == "deepseek":
        return OpenAI(
            api_key=st.secrets['DEEPSEEK_API_KEY'],
            base_url="https://api.deepseek.com/v1"
        )
    elif model == "grok":
        return OpenAI(
            api_key=st.secrets['GROK_API_KEY'],
            base_url="https://api.x.ai/v1"
        )
    else:
        raise ValueError(f"Unknown model: {model}")
    

def GenerateResponse(client_key, model, prompt, temperature):
    if model == "gemini-2.5-flash" or model == "gemini-2.5-pro":
        #response = client_key.models.generate_content(
        #    model=model, contents=prompt
        #)
        if model == "gemini-2.5-pro":
            response = client_key.generate_content(prompt)
        else:
            response = client_key.generate_content(prompt, model=model, temperature=temperature)
        #return response.text.strip()
        return (getattr(response, "text", None) or "")
    
    elif model == "gpt-4o-mini" or model == "gpt-4o" or model == "gpt-5":
        if model == "gpt-5":
            temperature = min(temperature, 1.0)  
        response = client_key.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()    
    
    elif model == "deepseek":
        response = client_key.chat.completions.create(
            model="deepseek-chat",
            temperature=temperature,
            messages=[
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0].message.content.strip()

    elif model == "grok":    
        response = client_key.chat.completions.create(
            model="grok-4-latest",
            temperature=temperature,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

