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
    

def GenerateResponse(client_key, model, prompt):
    if model == "gemini-2.5-flash" or model == "gemini-2.5-pro":
        #response = client_key.models.generate_content(
        #    model=model, contents=prompt
        #)
        response = client_key.generate_content(prompt, model=model, temperature=1.5)
        #return response.text.strip()
        return (getattr(response, "text", None) or "")
    
    elif model == "gpt-4o-mini" or model == "gpt-4o" or model == "gpt-5":
        response = client_key.chat.completions.create(
            model=model,
            temperature=1.5,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    
    elif model == "deepseek":
        st.write("Debug: Attempting DeepSeek API call...")
        
        # Check if client is properly set up
        if client_key is None:
            st.error("Client not initialized")
            return None
            
        try:
            # Test with a simple prompt first
            test_response = client_key.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": "Say 'Hello'"}],
                max_tokens=10
            )
            st.write("Debug: Basic API test passed")
            
            # Now make the actual call
            response = client_key.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2048,
                stream=False
            )
            
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"DeepSeek API call failed: {e}")
            return None
    
    elif model == "grok":    
        response = client_key.chat.completions.create(
            model="grok-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

