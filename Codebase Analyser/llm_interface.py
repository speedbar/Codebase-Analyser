import json
import google.generativeai as genai
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_api_key():
    try:
        with open('config.json') as config_file:
            config = json.load(config_file)
            return config.get('gemini_api_key')
    except Exception as e:
        logging.error(f"Error loading API key: {e}")
        return None

def generate_response(prompt):
    try:
        api_key = load_api_key()
        if not api_key:
            raise ValueError("API key is not available.")
            
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        logging.info(f"Sending prompt to model: {prompt[:100]}...")

        response = model.generate_content(prompt)
        if response.text:
            return response.text
        else:
            return "No response from Gemini"
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return "Error generating response"
