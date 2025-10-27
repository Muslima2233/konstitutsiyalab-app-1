import streamlit as st
import os
import requests
import json

# 🔐 Hugging Face API kaliti
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# 🔗 Ishlaydigan model URL
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

# 🧠 Funksiya: AI javobini olish
def query_huggingface(prompt):
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 700, "temperature": 0.7}}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        return f"❌ Xato: {response.status_code} - {response.text}"
    try:
        data = response.json()
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]
        else:
            return json.dumps(data, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"⚠️ Xatolik: {str(e)}"

# 🎯 Streamlit interfeysi
st.title("🇺🇿 KonstitutsiyaLab – AI yordamida test va kazus yaratish")

bo_lim = st.sidebar.radio("Bo‘limni tanlang:", ["Testlar", "Kazuslar"])

# 🔹 TESTLAR
if bo_lim == "Testlar":
    st.header("🧠 Konstitutsiya bo‘yicha test yaratish")
    topic = st.text_input("Mavzu nomini kiriting (masalan: 'Prezident vakolatlari')")
    
    if st.button("Test yaratish"):
        if not topic:
            st.warning("⚠️ Iltimos, mavzuni kiriting.")
        else:
            with st.spinner("AI test tayyorlayapti..."):
                prompt = f"O‘zbekiston Respublikasi 2023-yilgi Konstitutsiyasi asosida '{topic}' mavzusida 5 ta test savoli yozing. Har bir savolda 4 ta variant (A–D) bo‘lsin va oxirida to‘g‘ri javobni yozing."
                result = query_huggingface(prompt)
                st.text_area("📋 AI tomonidan yaratilgan testlar:", result, height=300)

# 🔹 KAZUSLAR
elif bo_lim == "Kazuslar":
    st.header("⚖️ Huquqiy kazus yaratish")
    topic = st.text_input("Kazus mavzusini kiriting (masalan: 'Fuqarolik huquqi')")
    
    if st.button("Kazus yaratish"):
        if not topic:
            st.warning("⚠️ Iltimos, mavzuni kiriting.")
        else:
            with st.spinner("AI kazus tayyorlayapti..."):
                prompt = f"O‘zbekiston Respublikasi 2023-yilgi Konstitutsiyasi asosida '{topic}' mavzusida real hayotga o‘xshash murakkab huquqiy kazus yozing va oxirida tahlilini bering."
                result = query_huggingface(prompt)
                st.write(result)
