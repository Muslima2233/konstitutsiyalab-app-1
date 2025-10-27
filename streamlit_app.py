import streamlit as st
import os
from huggingface_hub import InferenceClient

# 🔐 Hugging Face API kalitini olamiz (GitHub Secrets orqali)
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# API orqali AI mijozini chaqirish
client = InferenceClient(api_key=HUGGINGFACE_API_KEY)

st.title("🇺🇿 Konstitutsiya Asosidagi AI Platforma")

st.sidebar.title("Bo‘limni tanlang:")
section = st.sidebar.radio("Tanlang", ["Testlar", "Kazuslar", "Muhim ma’lumotlar"])

if section == "Testlar":
    st.header("🧠 Konstitutsiya bo‘yicha test yaratish")
    topic = st.text_input("Test mavzusini kiriting (masalan: 'O‘zbekiston Respublikasi Prezidenti')")
    if st.button("Test yaratish"):
        with st.spinner("AI test tayyorlayapti..."):
            response = client.text_generation(
                model="gpt2",  # vaqtincha oddiy model, keyin kuchlisiga almashtiramiz
                prompt=f"O‘zbekiston Respublikasi Konstitutsiyasi asosida {topic} mavzusi bo‘yicha 5 ta test savoli tuz.",
                max_new_tokens=300
            )
            st.write(response)

elif section == "Kazuslar":
    st.header("⚖️ Huquqiy kazus yaratish")
    topic = st.text_input("Kazus mavzusini kiriting (masalan: 'Fuqarolik huquqi')")
    if st.button("Kazus yaratish"):
        with st.spinner("AI kazus tayyorlayapti..."):
            response = client.text_generation(
                model="gpt2",
                prompt=f"O‘zbekiston Respublikasi Konstitutsiyasi asosida {topic} mavzusida bir murakkab huquqiy kazus yoz.",
                max_new_tokens=300
            )
            st.write(response)

elif section == "Muhim ma’lumotlar":
    st.header("📘 Konstitutsiyaning muhim ma’lumotlari")
    st.markdown("""
    - **Qabul qilingan sana:** 2023-yil 1-may  
    - **Bo‘limlar soni:** 7 ta  
    - **Moddalar soni:** 155 ta  
    - **Muddatlar:** Prezident — 7 yilga, Senat a’zolari — 5 yilga.  
    - **Qismlar:**  
        - Konstitutsiyaning 1/3 qismi – Asosiy tamoyillar  
        - 2/3 qismi – Davlat tuzilishi va inson huquqlari  
    """)

