import streamlit as st
from huggingface_hub import InferenceClient
import os

st.title("🔍 Hugging Face API sinovi")

token = os.getenv("HUGGINGFACE_API_KEY")
st.write("🔑 API kalit mavjudmi:", bool(token))

if token:
    st.success("✅ API kalit topildi!")
else:
    st.error("❌ API kalit topilmadi — Streamlit secrets sozlamasini tekshiring.")
