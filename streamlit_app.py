import streamlit as st
import os
from huggingface_hub import InferenceClient

# 🔐 Hugging Face API kalitini olish
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# AI modelga ulanamiz
client = InferenceClient(
    model="tiiuae/falcon-7b-instruct",
    token=HUGGINGFACE_API_KEY
)

st.title("🇺🇿 Konstitutsiya Asosidagi AI Platforma")

st.sidebar.title("Bo‘limni tanlang:")
section = st.sidebar.radio("Tanlang", ["Testlar", "Kazuslar", "Muhim ma’lumotlar"])

if section == "Testlar":
    st.header("🧠 Konstitutsiya bo‘yicha test yaratish")
    topic = st.text_input("Test mavzusini kiriting (masalan: 'Prezident vakolatlari')")
    if st.button("Test yaratish"):
        with st.spinner("AI test tayyorlayapti..."):
            prompt = f"O‘zbekiston Respublikasi 2023-yilgi Konstitutsiyasi asosida {topic} mavzusi bo‘yicha 5 ta test savoli va javoblarini tuz."
            response = client.text_generation(prompt=prompt, max_new_tokens=500)
            st.write(response)

elif section == "Kazuslar":
    st.header("⚖️ Huquqiy kazus yaratish")
    topic = st.text_input("Kazus mavzusini kiriting (masalan: 'Fuqarolik huquqi')")
    if st.button("Kazus yaratish"):
        with st.spinner("AI kazus tayyorlayapti..."):
            prompt = f"O‘zbekiston Respublikasi 2023-yilgi Konstitutsiyasi asosida {topic} mavzusida bir huquqiy kazus yoz. Kazus murakkab, o‘ylantiradigan bo‘lsin, lekin javobi ham bo‘lsin."
            response = client.text_generation(prompt=prompt, max_new_tokens=700)
            st.write(response)

elif section == "Muhim ma’lumotlar":
    st.header("📘 Konstitutsiyaning muhim ma’lumotlari")
    st.markdown("""
    - **Qabul qilingan sana:** 2023-yil 1-may  
    - **Bo‘limlar soni:** 7 ta  
    - **Moddalar soni:** 155 ta  
    - **Prezident vakolati muddati:** 7 yil  
    - **Qonun qabul qilish:** Qonun loyihasi qonunchilik palatasi tomonidan qabul qilinadi va Senat tomonidan ma’qullanadi.  
    - **Asosiy tamoyillar:** Suverenitet, demokratiya, ijtimoiy adolat, qonun ustuvorligi.
    """)
