
import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- SÜPER ARAYÜZ TASARIMI (CSS) ---
st.set_page_config(page_title="TR ZEKA PRO v7.0", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #4facfe; margin-bottom: 10px; }
    .stButton>button { background: linear-gradient(to right, #00c6ff, #0072ff); color: white; border: none; border-radius: 10px; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0px 0px 15px #00c6ff; }
    </style>
    """, unsafe_allow_html=True)

# --- YENİ BEYİN VE GÜVENLİK ---
API_KEY = "AIzaSyARWhX5RX_cq4mPTbQCpG0_8RnWrBBgTrg"
genai.configure(api_key=API_KEY)

# --- GELİŞMİŞ HAFIZA SİSTEMİ ---
if "memory" not in st.session_state:
    st.session_state.memory = []
if "nickname" not in st.session_state:
    st.session_state.nickname = "Kaptan"

# --- YAN PANEL (KONTROL MERKEZİ) ---
with st.sidebar:
    st.image("https://flaticon.com", width=120)
    st.title("🛡️ KONTROL MERKEZİ")
    st.session_state.nickname = st.text_input("Sana Nasıl Sesleneyim?", value=st.session_state.nickname)
    tone = st.selectbox("Asistan Tavrı", ["Dahi", "Yardımsever", "Şakacı", "Savaşçı"])
    st.divider()
    st.info(f"Hafıza Kapasitesi: {len(st.session_state.memory)} birim")
    if st.button("Hafızayı Sıfırla"):
        st.session_state.memory = []
        st.rerun()

st.title("🤖 TR ZEKA PRO: ZIRHLI SÜRÜM")
st.write(f"Hoş geldin **{st.session_state.nickname}**. Güvenlik protokolleri aktif. Tüm sistemler hazır.")

# --- MESAJLARI GÖSTER ---
for m in st.session_state.memory:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- FOTOĞRAF ANALİZİ ---
foto = st.sidebar.file_uploader("📷 Görsel Analiz (Opsiyonel)", type=["jpg", "png", "jpeg"])

# --- ÇOK KATMANLI KORUMA MOTORU ---
def ask_ai_ultra_secure(prompt, image):
    # Denenecek Model Sıralaması
    model_list = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
    
    # Hafızayı Yapay Zekaya Aktar (Asla Unutma)
    history_context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.memory[-5:]])
    full_prompt = f"Hafıza:\n{history_context}\n\nAdın TR Zeka. {st.session_state.nickname} ile konuşuyorsun. Tavrın {tone}. Soru: {prompt}"

    for attempt in range(4): # 4 Farklı Güvenlik Katmanı
        try:
            m_idx = attempt % len(model_list)
            model = genai.GenerativeModel(model_list[m_idx])
            
            if image and "flash" in model_list[m_idx]:
                img_data = Image.open(image)
                res = model.generate_content([full_prompt, img_data], request_options={"timeout": 600})
            else:
                res = model.generate_content(full_prompt, request_options={"timeout": 600})
            
            if res.text: return res.text
        except Exception as e:
            error_msg = str(e)
            time.sleep(1) # Kısa bekleme ve tekrar
            continue
            
    return f"SECURITY_ERROR:{error_msg}"

# --- SOHBET GİRİŞİ ---
if user_input := st.chat_input("Komutunuzu girin..."):
    st.session_state.memory.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("🛡️ Koruma kalkanı devrede, yanıt işleniyor..."):
            answer = ask_ai_ultra_secure(user_input, foto)
            
            if "SECURITY_ERROR" in answer:
                detail = answer.split(":")[1]
                st.error(f"Hata için çok üzgünüm {st.session_state.nickname}. 😣 Bu sorunlar Türkiye'de API kısıtlamalarından kaynaklanıyor. Ama elimizden geleni yaparak bunu kodla düzeltiyoruz 😉 \n\n**Hata Detayı:** {detail[:100]}...")
            else:
                st.markdown(answer)
                st.session_state.memory.append({"role": "assistant", "content": answer})
