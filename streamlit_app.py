import streamlit as st
import os
import requests

st.title("🇺🇿 KonstitutsiyaLab – AI yordamida test va kazus yaratish")

# API kalitni olish
api_key = os.getenv("HUGGINGFACE_API_KEY")
if not api_key:
    st.error("❌ API kaliti topilmadi. Iltimos, Streamlit Secrets ichiga HUGGINGFACE_API_KEY ni qo‘shing.")
    st.stop()

# Model nomi (ishlaydigan model)
model = "mistralai/Mistral-7B-Instruct-v0.3"
api_url = f"https://api-inference.huggingface.co/models/{model}"
headers = {"Authorization": f"Bearer {api_key}"}

# Bo‘lim tanlash
section = st.sidebar.radio("Bo‘limni tanlang:", ["🧠 Test yaratish", "⚖️ Kazus yaratish"])

# TEST BO‘LIMI
if section == "🧠 Test yaratish":
    st.subheader("Test yaratish")
    topic = st.text_input("Mavzu nomini kiriting:")
    if st.button("Test yaratish"):
        if not topic:
            st.warning("Iltimos, mavzu nomini kiriting!")
        else:
            prompt = f"O‘zbekiston Respublikasi Konstitutsiyasi asosida '{topic}' mavzusida 5 ta test savoli tuzing. Har biri 4 ta variantli (A–D) bo‘lsin va oxirida to‘g‘ri javobni ko‘rsating."
            with st.spinner("AI test tayyorlayapti..."):
                payload = {"inputs": prompt, "parameters": {"max_new_tokens": 600, "temperature": 0.7}}
                response = requests.post(api_url, headers=headers, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    try:
                        st.text_area("Natija:", result[0]["generated_text"], height=400)
                    except Exception:
                        st.write(result)
                else:
                    st.error(f"Xato yuz berdi: {response.text}")

# KAZUS BO‘LIMI
elif section == "⚖️ Kazus yaratish":
    st.subheader("Kazus yaratish")
    topic = st.text_input("Kazus mavzusi:")
    if st.button("Kazus yaratish"):
        if not topic:
            st.warning("Iltimos, kazus mavzusini kiriting!")
        else:
            prompt = f"O‘zbekiston Respublikasi Konstitutsiyasi asosida '{topic}' mavzusida huquqiy kazus yozing va uni tahlil qiling."
            with st.spinner("AI kazus tayyorlayapti..."):
                payload = {"inputs": prompt, "parameters": {"max_new_tokens": 700, "temperature": 0.7}}
                response = requests.post(api_url, headers=headers, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    try:
                        st.text_area("Natija:", result[0]["generated_text"], height=400)
                    except Exception:
                        st.write(result)
                else:
                    st.error(f"Xato yuz berdi: {response.text}")
