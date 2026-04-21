import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="TR Zeka Pro", page_icon="🤖")

# --- API AYARI ---
API_KEY = "AIzaSyAnicoAbklZ934WeLKaOcYF25qiZBpCqkQ"
genai.configure(api_key=API_KEY)

# --- SOHBET GEÇMİŞİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Arka planda modelleri tara ve en sağlamını bul
def get_ai_response(prompt, file):
    # Denenecek tüm model isim varyasyonları
    try_list = ["gemini-1.5-flash", "models/gemini-1.5-flash", "gemini-pro", "models/gemini-pro"]
    
    for model_name in try_list:
        try:
            model = genai.GenerativeModel(model_name)
            instr = f"Senin adın TR Zeka. Kullanıcıya seçtiği isimle hitap et. Soru: "
            
            if file and ("flash" in model_name):
                img = Image.open(file)
                response = model.generate_content([instr + prompt, img])
            else:
                response = model.generate_content(instr + prompt)
            
            return response.text
        except:
            continue # Hata verirse pes etme, bir sonrakini dene
    
    return None # Hiçbiri çalışmazsa

# --- ARAYÜZ ---
st.title("🤖 TR ZEKA WEB")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

file = st.sidebar.file_uploader("📷 Resim Analizi", type=["jpg", "png", "jpeg"])
nickname = st.sidebar.text_input("Adın ne olsun?", "Dostum")

if prompt := st.chat_input("Mesajınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_text = get_ai_response(prompt, file)
        
        if response_text:
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        else:
            st.error(f"Hata verdiğim için özür dilerim ama bağlantı sorunu beni durdurdu {nickname}. Lütfen VPN açıp veya API anahtarını kontrol edip tekrar dene!")

