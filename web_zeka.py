
import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="TR ZEKA PRO", page_icon="🤖")

# --- API AYARI ---
API_KEY = "AIzaSyAnicoAbklZ934WeLKaOcYF25qiZBpCqkQ"
genai.configure(api_key=API_KEY)

# --- YAN PANEL (AYARLAR) ---
with st.sidebar:
    st.title("⚙️ TR ZEKA AYARLARI")
    # Session State kullanarak ismi hafızada tutuyoruz
    if "nickname" not in st.session_state:
        st.session_state.nickname = "Dostum"
    
    st.session_state.nickname = st.text_input("Sana nasıl hitap edeyim?", value=st.session_state.nickname)
    tone = st.selectbox("Asistan Tavrı", ["Yardımsever", "Şakacı", "Ciddi", "Dahi"])
    
    st.divider()
    if st.button("Sohbeti Sıfırla"):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 TR ZEKA PRO v6.1")

# --- SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- FOTOĞRAF YÜKLEME ---
uploaded_file = st.sidebar.file_uploader("📷 Resim Analizi", type=["jpg", "png", "jpeg"])

# --- YAPAY ZEKA MOTORU ---
def ask_ai(prompt, file):
    # Denenecek modeller
    try_models = ["gemini-1.5-flash", "gemini-pro"]
    
    for m_name in try_models:
        try:
            model = genai.GenerativeModel(m_name)
            instr = f"Senin adın TR Zeka. Kullanıcıya '{st.session_state.nickname}' de. Tavrın '{tone}' olsun. "
            
            if file and "flash" in m_name:
                img = Image.open(file)
                response = model.generate_content([instr + prompt, img])
            else:
                response = model.generate_content(instr + prompt)
            
            # Yanıtın boş olup olmadığını kontrol et
            if response and response.text:
                return response.text
        except Exception as e:
            # Hata detayını terminale yaz ama kullanıcıya nazik davran
            print(f"Model {m_name} hatası: {e}")
            continue
            
    return "ERROR_STOPPED" # Hiçbiri çalışmazsa bu özel kodu döndür

# --- SORU-CEVAP ALANI ---
if prompt := st.chat_input("Mesajınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Düşünüyorum..."):
            ai_response = ask_ai(prompt, uploaded_file)
            
            if ai_response == "ERROR_STOPPED":
                # Senin istediğin o özel hata mesajı
                error_text = f"Hata verdiğim için özür dilerim ama bir bağlantı sorunu beni durdurdu {st.session_state.nickname}. Lütfen biraz bekleyip tekrar dene! 😅"
                st.error(error_text)
            else:
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
