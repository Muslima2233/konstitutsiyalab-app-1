import streamlit as st
import os
import requests
import json

# 🔐 Hugging Face API kaliti
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# 🧠 Barqaror ishlaydigan model
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def ask_huggingface(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 700, "temperature": 0.7}
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        return f"❌ Xato: {response.status_code} - {response.text}"
    try:
        data = response.json()
        return data[0]["generated_text"]
    except Exception as e:
        return f"⚠️ Xatolik: {str(e)}"

# 🌐 Streamlit interfeysi
st.title("🇺🇿 KonstitutsiyaLab – AI yordamida test va kazus yaratish")

bo_lim = st.sidebar.radio("Bo‘limni tanlang:", ["Testlar", "Kazuslar"])

# 🔹 TESTLAR BO‘LIMI
if bo_lim == "Testlar":
    st.header("🧠 Konstitutsiya bo‘yicha test yaratish")
    topic = st.text_input("Mavzu nomini kiriting:")
    
    if st.button("Test yaratish"):
        if not topic:
            st.warning("Iltimos, mavzuni kiriting!")
        else:
            with st.spinner("AI test tayyorlayapti..."):
                prompt = f"O‘zbekiston Respublikasi Konstitutsiyasi asosida '{topic}' mavzusida 5 ta test savoli yozing. Har bir savolda 4 ta variant (A–D) bo‘lsin va oxirida to‘g‘ri javobni yozing."
                result = ask_huggingface(prompt)
                st.text_area("🧾 AI tomonidan yaratilgan testlar:", result, height=300)

# 🔹 KAZUSLAR BO‘LIMI
elif bo_lim == "Kazuslar":
    st.header("⚖️ Huquqiy kazus yaratish")
    topic = st.text_input("Kazus mavzusini kiriting:")
    
    if st.button("Kazus yaratish"):
        if not topic:
            st.warning("Iltimos, mavzuni kiriting!")
        else:
            with st.spinner("AI kazus tayyorlayapti..."):
                prompt = f"O‘zbekiston Respublikasi 2023-yilgi Konstitutsiyasi asosida '{topic}' mavzusida murakkab huquqiy kazus yozing. Holatni real hayotga o‘xshatib yozing va oxirida tahlilini yozing."
                result = ask_huggingface(prompt)
                st.write(result)
