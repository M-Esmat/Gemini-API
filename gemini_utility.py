import os
import json

from keys import gemini_key

import google.generativeai as genai

from PIL import Image


working_dir = os.path.dirname(os.path.abspath(__file__))

# print(gemini_key)

# load api key

GOOGLE_API_KEY = gemini_key

# configure genai with api key

genai.configure(api_key= GOOGLE_API_KEY)

# function to load gemini for chatbot
def load_gemini_model():
    gemini_model = genai.GenerativeModel('gemini-2.0-flash')
    return gemini_model


# function for image captioning
def gemini_image_caption(prompt, image):
    gemini_vision_model = genai.GenerativeModel('gemini-2.0-flash')
    responese = gemini_vision_model.generate_content([prompt, image])
    result = responese.text
    return result

# image = Image.open("test_image1.jpeg")

# prompt = "write a short caption for this image"

# output = gemini_image_caption(prompt, image)
# print(output)


def gemini_embedding(input_text):
    #gemini_embed_model = genai.GenerativeModel('models/embedding-001')
    embedding = genai.embed_content(model='models/embedding-001', content=input_text,
                                    task_type='retrieval_document')
    return embedding

# output = gemini_embedding("Winter wonderland dreams! Cozy cabins, sparkling snow, and a friendly snowman to greet you. Where winter wishes come true.")
# print(output)

def  gemini_pro_response(input_text):
    #gemini_embed_model = genai.GenerativeModel('models/embedding-001')
    question_answer_model = genai.GenerativeModel('gemini-2.0-flash')
    response = question_answer_model.generate_content([input_text])
    result = response.text
    return result

# output = gemini_embedding("Winter wonderland dreams! Cozy cabins, sparkling snow, and a friendly snowman to greet you. Where winter wishes come true.")
# print(output)

def gemini_translator(text, from_lang="English", to_lang="German"):

    tranlator_prompt = (f"Translate the following text from {from_lang} to {to_lang}:\n\n"
                        f"\"{text}\"")
    
    translator_model = genai.GenerativeModel('gemini-2.0-flash')
    response = translator_model.generate_content([tranlator_prompt])
    return response.text

