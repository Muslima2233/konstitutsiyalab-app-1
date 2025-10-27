import streamlit as st
import os
from huggingface_hub import InferenceClient

# 🔐 Hugging Face API kalitini olish
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HUGGINGFACE_API_KEY:
    st.error("❌ Hugging Face API kaliti topilmadi. Replit Secrets'da 'HUGGINGFACE_API_KEY' nomi bilan kiriting.")
    st.stop()

# 🧠 Ishlaydigan model (barqaror)
MODEL_ID = "tiiuae/falcon-7b-instruct"
client = InferenceClient(model=MODEL_ID, token=HUGGINGFACE_API_KEY)

st.title("🇺🇿 Konstitutsiya Asosidagi AI Platforma")

st.sidebar.title("Bo‘limni tanlang:")
section = st.sidebar.radio("Tanlang", ["Testlar", "Kazuslar", "Muhim ma’lumotlar"])

# ----------------------------- TESTLAR -----------------------------
if section == "Testlar":
    st.header("🧠 Konstitutsiya bo‘yicha test yaratish")
    topic = st.text_input("Test mavzusini kiriting (masalan: 'Prezident vakolatlari')")

    if "generated_test" not in st.session_state:
        st.session_state.generated_test = ""

    if st.button("Test yaratish"):
        with st.spinner("AI test tayyorlayapti..."):
            prompt = f"O‘zbekiston Respublikasi Konstitutsiyasi asosida '{topic}' mavzusida 5 ta test savoli yozing. Har bir savolda 4 ta variant (A–D) bo‘lsin va oxirida to‘g‘ri javobni yozing."
            
            # 🔧 So‘rov yuborish (stabil variant)
            response = client.post(
                json={
                    "inputs": prompt,
                    "parameters": {"max_new_tokens": 700, "temperature": 0.7}
                }
            )
            text_output = response[0]["generated_text"].strip()
            st.session_state.generated_test = text_output
        
        st.success("✅ Test tayyor bo‘ldi!")

    if st.session_state.generated_test:
        st.write("📋 **AI tomonidan yaratilgan testlar:**")
        st.text_area("Testlar", st.session_state.generated_test, height=250)

        st.markdown("---")
        st.subheader("✍️ Javoblaringizni kiriting (masalan: 1-A, 2-B, 3-D ...)")
        user_answers = st.text_area("Sizning javoblaringiz")

        if st.button("Natijani tekshirish"):
            with st.spinner("AI javoblaringizni tekshirmoqda..."):
                check_prompt = f"Quyidagi testlar va foydalanuvchi javoblarini solishtirib, nechta to‘g‘ri javob borligini aniqlang va foizda baholang:\n\n{st.session_state.generated_test}\n\nFoydalanuvchi javoblari:\n{user_answers}"
                
                response = client.post(
                    json={
                        "inputs": check_prompt,
                        "parameters": {"max_new_tokens": 400, "temperature": 0.3}
                    }
                )
                result_text = response[0]["generated_text"].strip()
                st.success("✅ Natija:")
                st.write(result_text)

# ----------------------------- KAZUSLAR -----------------------------
elif section == "Kazuslar":
    st.header("⚖️ Huquqiy kazus yaratish")
    topic = st.text_input("Kazus mavzusini kiriting (masalan: 'Fuqarolik huquqi')")

    if st.button("Kazus yaratish"):
        with st.spinner("AI kazus tayyorlayapti..."):
            prompt = f"O‘zbekiston Respublikasi 2023-yilgi Konstitutsiyasi asosida '{topic}' mavzusida murakkab huquqiy kazus yozing. Kazus real hayotga o‘xshash bo‘lsin va oxirida uning tahlilini yozing."
            
            response = client.post(
                json={
                    "inputs": prompt,
                    "parameters": {"max_new_tokens": 900, "temperature": 0.8}
                }
            )
            kazus_text = response[0]["generated_text"].strip()
            st.write(kazus_text)

# ----------------------------- MUHIM MA'LUMOTLAR -----------------------------
elif section == "Muhim ma’lumotlar":
    st.header("📘 Konstitutsiyaning muhim ma’lumotlari")
    st.markdown("""
    - **Qabul qilingan sana:** 2023-yil 1-may  
    - **Bo‘limlar soni:** 7 ta  
    - **Moddalar soni:** 155 ta  
    - **Prezident vakolati muddati:** 7 yil  
    - **Qonun qabul qilish:** Qonun loyihasi Qonunchilik palatasi tomonidan qabul qilinadi va Senat tomonidan ma’qullanadi.  
    - **Asosiy tamoyillar:** Suverenitet, demokratiya, ijtimoiy adolat, qonun ustuvorligi.
    """)
