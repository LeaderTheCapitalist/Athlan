import streamlit as st
import requests
import json
from datetime import datetime

# ===== ENTER YOUR API KEY BELOW =====
OPENROUTER_API_KEY = "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"  # Replace with your actual key from https://openrouter.ai/keys

# Set page config FIRST
st.set_page_config(page_title="Sportify AI - Your AI Fitness Coach", layout="wide")

# Add custom CSS for cursor
st.markdown("""
    <style>
        /* Nuclear option for cursor - works on all interactive elements */
        div[data-baseweb="select"] div {
            cursor: pointer !important;
        }
        div[data-baseweb="select"] div[role="button"] {
            cursor: pointer !important;
        }
        div[role="listbox"] div {
            cursor: pointer !important;
        }
        /* Make sure buttons also have pointer */
        button {
            cursor: pointer !important;
        }
    </style>
""", unsafe_allow_html=True)

# Language dictionary
translations = {
    "English": {
        "title": "Sport",
        "subtitle": "Create your personalized training plan",
        "sport_placeholder": "e.g., Football, Soccer",
        "skill_level": "Skill Level",
        "skill_levels": ["Beginner", "Intermediate", "Advanced", "Professional"],
        "disabilities": "Disabilities",
        "disabilities_placeholder": "e.g., Amputee, Visual Impairment",
        "equipment": "Equipment Availability",
        "equipment_placeholder": "e.g., No equipment available, Access to equipment",
        "culture": "Cultural Preferences",
        "culture_placeholder": "e.g., Halal, Kosher",
        "diet": "Diet Plan",
        "diet_placeholder": "e.g., High protein, Vegetarian",
        "generate_btn": "Generate Plan",
        "spinner_text": "🧠 Designing your custom training plan...",
        "api_warning": "Please add your OpenRouter API key in the code!",
        "plan_title": "Your {} Plan ({})",
        "save_btn": "Save Plan",
        "error_message": "Failed to generate plan. Check your API key and try again.",
        "prompt_instruction": "Respond in English."
    },
    "Русский": {
        "title": "Спорт",
        "subtitle": "Создайте свой персональный план тренировок",
        "sport_placeholder": "напр., Футбол, Волейбол",
        "skill_level": "Уровень подготовки",
        "skill_levels": ["Новичок", "Любитель", "Опытный", "Профессионал"],
        "disabilities": "Ограничения",
        "disabilities_placeholder": "напр., Ампутация, Нарушение зрения",
        "equipment": "Доступное оборудование",
        "equipment_placeholder": "напр., Нет оборудования, Есть доступ к оборудованию",
        "culture": "Культурные/религиозные предпочтения",
        "culture_placeholder": "напр., Халяль, Кошер",
        "diet": "План питания",
        "diet_placeholder": "напр., Высокобелковая, Вегетарианская",
        "generate_btn": "Создать план",
        "spinner_text": "🧠 Создаем ваш индивидуальный план тренировок...",
        "api_warning": "Пожалуйста, добавьте ваш API ключ в код!",
        "plan_title": "Ваш план по {} ({})",
        "save_btn": "Сохранить план",
        "error_message": "Не удалось создать план. Проверьте API ключ и попробуйте снова.",
        "prompt_instruction": "Отвечайте на русском языке."
    },
    "O`zbek": {
        "title": "Sport",
        "subtitle": "Shaxsiy mashq rejangizni yarating",
        "sport_placeholder": "masalan, Futbol, Voleybol",
        "skill_level": "Mahorat darajasi",
        "skill_levels": ["Boshlang'ich", "O'rta", "Yuqori", "Professional"],
        "disabilities": "Nogironliklar",
        "disabilities_placeholder": "masalan, amputatsiya, ko'rish qiyinchiligi",
        "equipment": "Mavjud jihozlar",
        "equipment_placeholder": "masalan, Jihozlar mavjud emas, Jihozlar yetarli",
        "culture": "Madaniy/diniy afzalliklar",
        "culture_placeholder": "masalan, Halol, Kosher",
        "diet": "Ovqatlanish rejasi",
        "diet_placeholder": "masalan, Oqsilli, Vegetarian",
        "generate_btn": "Reja yaratish",
        "spinner_text": "🧠 Siz uchun maxsus mashq rejasi tayyorlanmoqda...",
        "api_warning": "Iltimos, kodga OpenRouter API kalitingizni qo'shing!",
        "plan_title": "Sizning {} rejangiz ({})",
        "save_btn": "Rejani saqlash",
        "error_message": "Reja yaratib bo'lmadi. API kalitingizni tekshirib, qayta urinib ko'ring.",
        "prompt_instruction": "Javobni o'zbek tilida bering."
    }
}

# Language selection in sidebar
with st.sidebar:
    language = st.selectbox("Language | Til | Язык", ["English", "O`zbek", "Русский"])

# Get current language strings
lang = translations[language]

# App UI
st.title(lang["title"])
st.caption(lang["subtitle"])

# User Inputs
with st.form("inputs"):
    col1, col2 = st.columns(2)
    with col1:
        sport = st.text_input(lang["title"], placeholder=lang["sport_placeholder"], key="sport")
        difficulty = st.select_slider(lang["skill_level"], lang["skill_levels"])
    with col2:
        disability = st.text_input(lang["disabilities"], placeholder=lang["disabilities_placeholder"])
        equipment = st.text_input(lang["equipment"], placeholder=lang["equipment_placeholder"])
        culture = st.text_input(lang["culture"], placeholder=lang["culture_placeholder"])
        diet = st.text_input(lang["diet"], placeholder=lang["diet_placeholder"])

    generate_btn = st.form_submit_button(lang["generate_btn"], type="primary")

# API Call Function
def call_deepseek(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "Fitness Plan Generator"
    }

    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1500
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=45
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        if hasattr(e, 'response') and e.response:
            st.error(f"Details: {e.response.text}")
        return None

# Generate Plan
if generate_btn and sport:
    if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "your_api_key_here":
        st.warning(lang["api_warning"])
    else:
        with st.spinner(lang["spinner_text"]):
            prompt = f"""{lang['prompt_instruction']}
            Create a {difficulty} level {sport} training plan for:
            - Physical needs: {disability if disability else "None"}
            - Cultural/religious: {culture if culture else "None"}
            - Equipment availability: {equipment if equipment else "None"}

            Include:
            1. Warm-up (dynamic exercises)
            2. Main workout (3-5 adapted exercises)
            3. Cooldown (static stretches)
            4. Safety precautions
            5. Equipment suggestions

            Format in markdown with bullet points."""

            result = call_deepseek(prompt)

            if result:
                plan = result["choices"][0]["message"]["content"]
                st.subheader(lang["plan_title"].format(sport, difficulty))
                st.markdown(plan)

                st.download_button(
                    label=lang["save_btn"],
                    data=plan,
                    file_name=f"{sport.replace(' ', '_')}_plan_{language}.md",
                    mime="text/markdown"
                )
            else:
                st.error(lang["error_message"])
