import streamlit as st
from streamlit_option_menu import option_menu

import os

import gemini_utility as gu

from PIL import Image
import io
from langdetect import detect, DetectorFactory
#from dotenv import load_dotenv


working_dir = os.path.dirname(os.path.abspath(__file__))

# print(working_dir)

# setting streamlit page configuration

st.set_page_config(
    page_title= "Gemini AI",
    page_icon= "🤖",
    layout= "centered",
)


with st.sidebar:
    
    selected= option_menu("Gemini AI",
                          ['Chatbot',
                           'Image Captioning',
                           'Embed text',
                           'Q&A',
                           'translator'],
                          menu_icon='robot', icons=['chat-dots-fill', 'card-image',
                                                    'card-text', 'question-octagon',
                                                    'translate'],
                          default_index= 0)
    


# change roles of gemini and stremlit
def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return 'assistant'
    else:
        return user_role
    
    

if selected == 'Chatbot':
    model = gu.load_gemini_model()
    
    # initialize chat and maintain chat sessions -- act as context for following prompts
    
    if 'chat_session' not in st.session_state: # create a chat session if not already created
        st.session_state.chat_session = model.start_chat(history=[])
    
    st.title('🤖 Chatbot')
    
    # display chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)
            
    # input for user message
    user_prompt = st.chat_input("Ask Gemini what you want .... ")
    
    if user_prompt:
        st.chat_message('user').markdown(user_prompt)
        
        # send user prompt to model
        gemini_respond = st.session_state.chat_session.send_message(user_prompt)
        
        # display model response
        with st.chat_message('assistant'):
            st.markdown(gemini_respond.text)
    

if selected == 'Image Captioning':
    
    
    # streamlit page
    
    st.title("📷 Image Captioner")
    
    upload_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
    
    # enter user prompt
    user_prompt = st.text_input("Enter a prompt for the image captioner (optional) ... ")
    if st.button('Generate Caption'):
        
        #st.write("Uploaded file:", upload_image)

        image = Image.open(upload_image)
        
        col1, col2 = st.columns(2)
        
        with col1:
            resized_image = image.resize((800, 500))
            st.image(resized_image)
        
        
        default_prompt = "Write a short caption for this image"
        # if the user don't write a caption the field will be empty string --> use default
        final_prompt = user_prompt.strip() if user_prompt.strip() != "" else default_prompt
        
        # getting response from gemini
        caption = gu.gemini_image_caption(final_prompt, resized_image)
        
        with col2:
            st.info(caption)
        
        
        
        
# embedding page
if selected == 'Embed text':
    
    st.title("🗟 text embeddings")
    
    input_text = st.text_area(label= '', placeholder= 'Enter the ext to get the embeddings')
    
    if st.button("get embeddings"):
        response = gu.gemini_embedding(input_text)
        st.markdown(response)


if selected == 'Q&A':
    
    st.title("❓ Ask me a question")

    # text box to enter prompt
    user_prompt = st.text_area(label='', placeholder="Ask me anything...")

    if st.button("Get Response"):
        response = gu.gemini_pro_response(user_prompt)
        st.markdown(response)

if selected == 'translator':
    st.title("🔤 Translator")
    # Set seed for reproducibility of language detection
    DetectorFactory.seed = 42

# Define list of languages. Note that langdetect returns ISO 639-1 codes,
# so we need to map them to the names used in your options.
    language_mapping = {
        "en": "English",
        "de": "German",
        "fr": "French",
        "es": "Spanish",
        "ar": "Arabic",
        "zh-cn": "Chinese",
        "ja": "Japanese",
        "ru": "Russian",
        "it": "Italian",
        "pt": "Portuguese"}
    languages = [ "English", "German", "French", "Spanish", "Arabic", "Chinese", "Japanese", "Russian", "Italian", "Portuguese" ]
    st.markdown("Translate between languages using Google's Gemini model.")

    col1, col2 = st.columns(2)
    
    with col1:
        from_lang = st.selectbox("Translate From:", options=languages, index=0)
    with col2:
        to_lang = st.selectbox("Translate To:", options=languages, index=1)

    input_text = st.text_area(label="", placeholder=f"Type your {from_lang} sentence here...")

    if st.button("Translate"):
        if input_text.strip() == "":
            st.warning("⚠️ Please enter a sentence to translate.")
        elif from_lang == to_lang:
            st.info("🤔 Source and target languages are the same.")
        else:
            try:
                detected_code = detect(input_text)
                detected_language = language_mapping.get(detected_code, "Unknown")
            except Exception as e:
                st.error("❌ Failed to detect language. Please ensure your input text is valid.")
                detected_language = "Unknown"
            
            if detected_language != from_lang:
                st.error(f"⚠️ Input text is detected as **{detected_language}**, but 'Translate From' is set to **{from_lang}**. Please check your input or change the source language.")
            else:
                translation = gu.gemini_translator(input_text, from_lang=from_lang, to_lang=to_lang)
                st.success("**Translation:**")
                st.markdown(translation)