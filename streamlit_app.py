import streamlit as st
import os
from huggingface_hub import InferenceClient

# 🔐 API kalitni olish
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HUGGINGFACE_API_KEY:
    st.error("❌ API kaliti topilmadi. Streamlit Secrets orqali kiriting.")
    st.stop()

# ✅ Ishlaydigan model (togethercomputer/LLaMA-2 7B)
MODEL_ID = "HuggingFaceH4/zephyr-7b-beta"
client = InferenceClient(model=MODEL_ID, token=HUGGINGFACE_API_KEY)

st.title("🇺🇿 Konstitutsiya Asosidagi AI Platforma")

section = st.sidebar.radio("Bo‘limni tanlang:", ["Testlar", "Kazuslar"])

if section == "Testlar":
    st.header("🧠 Test yaratish")
    topic = st.text_input("Test mavzusini kiriting:")

    if st.button("Test yaratish"):
        with st.spinner("AI test tayyorlayapti..."):
            prompt = f"O‘zbekiston Respublikasi Konstitutsiyasi asosida '{topic}' mavzusida 5 ta test savoli yozing, har biri 4 variantli (A-D), oxirida to‘g‘ri javobni yozing."
            response = client.text_generation(prompt, max_new_tokens=700)
            st.text_area("Natija", response, height=300)

elif section == "Kazuslar":
    st.header("⚖️ Kazus yaratish")
    topic = st.text_input("Kazus mavzusi:")
    if st.button("Kazus yaratish"):
        with st.spinner("AI kazus tayyorlayapti..."):
            prompt = f"O‘zbekiston Konstitutsiyasi asosida '{topic}' mavzusida huquqiy kazus yozing va uni tahlil qiling."
            response = client.text_generation(prompt, max_new_tokens=700)
            st.write(response)
