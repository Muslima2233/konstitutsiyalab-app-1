import streamlit as st
import os
from huggingface_hub import InferenceClient

# 🔐 Hugging Face API kalitini olish
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# 🧠 Ishlaydigan modelni ulaymiz (Llama3 model)
client = InferenceClient(
    model="meta-llama/Llama-3.1-8B-Instruct",
    token=HUGGINGFACE_API_KEY
)

st.title("🇺🇿 Konstitutsiya Asosidagi AI Platforma")

st.sidebar.title("Bo‘limni tanlang:")
section = st.sidebar.radio("Tanlang", ["Testlar", "Kazuslar", "Muhim ma’lumotlar"])

# 🔹 TESTLAR BO‘LIMI
if section == "Testlar":
    st.header("🧠 Konstitutsiya bo‘yicha test yaratish")
    topic = st.text_input("Test mavzusini kiriting (masalan: 'Prezident vakolatlari')")

    if "generated_test" not in st.session_state:
        st.session_state.generated_test = ""

    if st.button("Test yaratish"):
        if not topic.strip():
            st.warning("Iltimos, test mavzusini kiriting.")
        else:
            with st.spinner("AI test tayyorlayapti..."):
                prompt = f"O‘zbekiston Respublikasi Konstitutsiyasi asosida '{topic}' mavzusida 5 ta test savoli yozing. Har bir savol uchun 4 ta variant (A–D) yozing va to‘g‘ri javobni oxirida 'To‘g‘ri javob:' deb belgilang."
                response = client.text_generation(
                    prompt,
                    max_new_tokens=700,
                    temperature=0.7,
                )
                st.session_state.generated_test = response.generated_text.strip()
            st.success("✅ Test tayyor bo‘ldi!")

    if st.session_state.generated_test:
        st.write("📋 **AI tomonidan yaratilgan testlar:**")
        st.text_area("Testlar", st.session_state.generated_test, height=250)

        st.markdown("---")
        st.subheader("✍️ Javoblaringizni kiriting (masalan: 1-A, 2-B, 3-D ...)")
        user_answers = st.text_area("Sizning javoblaringiz")

        if st.button("Natijani tekshirish"):
            with st.spinner("AI javoblaringizni tekshirmoqda..."):
                check_prompt = f"Quyidagi testlar va foydalanuvchi javoblarini solishtirib, nechta to‘g‘ri javob bo‘lganini aniqlang va baho qo‘ying (foiz bilan):\n\nTestlar:\n{st.session_state.generated_test}\n\nFoydalanuvchi javoblari:\n{user_answers}"
                result = client.text_generation(
                    check_prompt,
                    max_new_tokens=500,
                    temperature=0.3
                )
                st.success("✅ Natija:")
                st.write(result.generated_text.strip())

# 🔹 KAZUSLAR BO‘LIMI
elif section == "Kazuslar":
    st.header("⚖️ Huquqiy kazus yaratish")
    topic = st.text_input("Kazus mavzusini kiriting (masalan: 'Fuqarolik huquqi')")

    if st.button("Kazus yaratish"):
        if not topic.strip():
            st.warning("Iltimos, kazus mavzusini kiriting.")
        else:
            with st.spinner("AI kazus tayyorlayapti..."):
                prompt = f"O‘zbekiston Respublikasi 2023-yilgi Konstitutsiyasi asosida '{topic}' mavzusida murakkab huquqiy kazus yozing. Kazus real hayotga o‘xshash bo‘lsin va oxirida uning tahlilini yozing."
                response = client.text_generation(
                    prompt,
                    max_new_tokens=800,
                    temperature=0.8
                )
                st.success("✅ Kazus tayyor bo‘ldi!")
                st.write(response.generated_text.strip())

# 🔹 MUHIM MA'LUMOTLAR BO‘LIMI
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
