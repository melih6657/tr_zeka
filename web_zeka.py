
import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="TR ZEKA PRO", page_icon="🤖")

# --- API YAPILANDIRMASI ---
API_KEY = "AIzaSyAnicoAbklZ934WeLKaOcYF25qiZBpCqkQ"
genai.configure(api_key=API_KEY)

# --- AYARLAR VE HAFIZA ---
if "nickname" not in st.session_state:
    st.session_state.nickname = "Dostum"

with st.sidebar:
    st.title("⚙️ AYARLAR")
    st.session_state.nickname = st.text_input("Sana nasıl hitap edeyim?", value=st.session_state.nickname)
    tone = st.selectbox("Asistan Tavrı", ["Yardımsever", "Şakacı", "Ciddi", "Dahi"])
    if st.button("Sohbeti Sıfırla"):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 TR ZEKA PRO v6.2")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

uploaded_file = st.sidebar.file_uploader("📷 Resim Analizi", type=["jpg", "png", "jpeg"])

# --- BAĞLANTIYI DÜZELTEN ANA MOTOR ---
def ask_ai_secure(prompt, file):
    # Denenecek modeller ve bağlantı varyasyonları
    try_models = ["gemini-1.5-flash", "gemini-pro", "models/gemini-1.5-flash", "models/gemini-pro"]
    
    # Her model için 2 kez deneme (Toplam 8 deneme yapar)
    for m_name in try_models:
        for attempt in range(2): 
            try:
                model = genai.GenerativeModel(m_name)
                instr = f"Senin adın TR Zeka. Kullanıcıya '{st.session_state.nickname}' de. Tavrın '{tone}' olsun. "
                
                if file and "flash" in m_name:
                    img = Image.open(file)
                    response = model.generate_content([instr + prompt, img], request_options={"timeout": 600})
                else:
                    response = model.generate_content(instr + prompt, request_options={"timeout": 600})
                
                if response and response.text:
                    return response.text
            except Exception as e:
                print(f"Deneme Başarısız ({m_name}, Tekrar: {attempt}): {e}")
                time.sleep(1) # Bağlantı hatasında 1 saniye bekle ve tekrar dene
                continue
                
    return "CONNECTION_FAILED"

# --- SORU-CEVAP DÖNGÜSÜ ---
if prompt := st.chat_input("Mesajınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Sunucuya bağlanıyorum, lütfen bekleyin... 🚀"):
            ai_response = ask_ai_secure(prompt, uploaded_file)
            
            if ai_response == "CONNECTION_FAILED":
                # İstediğin nazik hata mesajı
                error_text = f"Hata verdiğim için özür dilerim ama bağlantı sorunu beni durdurdu {st.session_state.nickname}. Sunucuya şu an ulaşamıyorum, lütfen kısa süre sonra tekrar dene! 😅"
                st.error(error_text)
            else:
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
