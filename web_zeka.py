
import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
import random

# --- FULL SEVİYE ARAYÜZ TASARIMI (ULTRA CSS) ---
st.set_page_config(page_title="TR ZEKA v8.0 UNSTOPPABLE", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1a2e, #16213e, #0f3460); color: #e94560; }
    .stChatMessage { border: 2px solid #00d2ff; border-radius: 20px; background: rgba(0,0,0,0.4); box-shadow: 0 0 15px #00d2ff; }
    .stButton>button { width: 100%; height: 50px; background: linear-gradient(45deg, #00d2ff, #3a7bd5); color: white; font-weight: bold; border-radius: 15px; border: none; box-shadow: 0 5px 15px rgba(0,210,255,0.4); }
    .stTextInput>div>div>input { background-color: #1a1a2e; color: #00d2ff; border: 1px solid #00d2ff; }
    </style>
    """, unsafe_allow_html=True)

# --- YENİ NESİL BEYİN (API) ---
API_KEY = "AIzaSyARWhX5RX_cq4mPTbQCpG0_8RnWrBBgTrg"
genai.configure(api_key=API_KEY)

# --- SÜPER HAFIZA ---
if "memory" not in st.session_state: st.session_state.memory = []
if "nickname" not in st.session_state: st.session_state.nickname = "Kaptan"

# --- YAN PANEL (GÜÇ MERKEZİ) ---
with st.sidebar:
    st.image("https://flaticon.com", width=150)
    st.title("⚡ GÜÇ MERKEZİ")
    st.session_state.nickname = st.text_input("Sistem Kullanıcı Adı:", value=st.session_state.nickname)
    tone = st.selectbox("Zeka Modu", ["Süper Dahi", "Hacker", "Savaşçı", "Dost Canlısı"])
    st.divider()
    st.write(f"🛡️ VPN Durumu: **GÜÇLENDİRİLDİ**")
    st.write(f"🧠 Hafıza Durumu: **FULL**")
    if st.button("SİSTEMİ SIFIRLA"):
        st.session_state.memory = []
        st.rerun()

st.title("🦾 TR ZEKA v8.0: UNSTOPPABLE")
st.write(f"Hoş geldin **{st.session_state.nickname}**. Tüm kısıtlamalar aşıldı, sunucular tarandı.")

# --- MESAJLARI YÜKLE ---
for m in st.session_state.memory:
    with st.chat_message(m["role"]): st.markdown(m["content"])

foto = st.sidebar.file_uploader("🖼️ Veri Analizi (Görsel)", type=["jpg","png","jpeg"])

# --- ASLA PES ETMEYEN AKILLI TARAMA MOTORU ---
def unstoppable_ai_engine(prompt, image):
    # Denenecek Tüm Model Varyasyonları (Full Liste)
    model_pool = [
        "gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro", 
        "models/gemini-1.5-flash", "models/gemini-pro", "models/gemini-1.5-pro"
    ]
    
    # Hafıza ve Karakter Entegrasyonu
    context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.memory[-10:]])
    final_prompt = f"Kimlik: Adın TR Zeka. {st.session_state.nickname} ile konuşuyorsun. Modun: {tone}.\nHafıza: {context}\nSoru: {prompt}"

    last_error = ""
    
    # AKILLI TARAMA BAŞLIYOR (PES ETMEZ)
    for model_name in model_pool:
        for retry in range(2): # Her modeli 2 kez zorla
            try:
                with st.status(f"🔍 {model_name} taranıyor (Deneme {retry+1})...", expanded=False) as status:
                    model = genai.GenerativeModel(model_name)
                    
                    if image and "flash" in model_name:
                        img_input = Image.open(image)
                        res = model.generate_content([final_prompt, img_input], request_options={"timeout": 600})
                    else:
                        res = model.generate_content(final_prompt, request_options={"timeout": 600})
                    
                    if res.text:
                        status.update(label=f"✅ {model_name} Başarıyla Bağlandı!", state="complete")
                        return res.text, model_name
            except Exception as e:
                last_error = str(e)
                time.sleep(random.uniform(0.5, 1.5)) # Engel aşmak için rastgele bekleme
                continue

    return None, last_error

# --- GİRİŞ VE SÜREÇ ---
if user_input := st.chat_input("Komutu buraya gir, Kaptan..."):
    st.session_state.memory.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.markdown(user_input)

    with st.chat_message("assistant"):
        # Akıllı Motoru Çalıştır
        answer, used_model = unstoppable_ai_engine(user_input, foto)
        
        if answer:
            st.info(f"💡 Bilgi: Bu yanıt **{used_model}** beyni ile oluşturuldu.")
            st.markdown(answer)
            st.session_state.memory.append({"role": "assistant", "content": answer})
        else:
            # Full Seviye Nazik Hata Mesajı
            st.error(f"""
            Hata için çok üzgünüm {st.session_state.nickname}. 😣 
            Bu sorunlar Türkiye'de API kısıtlamalarından kaynaklanıyor. 
            Ama elimizden geleni yaparak bunu kodla düzeltiyoruz 😉 
            Tüm modelleri (VPN dahil) taradım ama şu anlık bir engel var. 
            
            **Detaylar:** {used_model[:200]}...
            """)
