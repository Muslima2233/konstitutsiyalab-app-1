import streamlit as st
from huggingface_hub import InferenceClient
import os

st.title("🔍 Hugging Face API sinovi")

token = os.getenv("HUGGINGFACE_API_KEY")
st.write("🔑 API kalit mavjudmi:", bool(token))

try:
    client = InferenceClient(token=token)
    models = client.list_models(limit=1)
    st.success("✅ API kalit ishlayapti!")
except Exception as e:
    st.error(f"❌ Xato: {e}")
