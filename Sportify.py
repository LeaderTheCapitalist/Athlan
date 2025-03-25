import streamlit as st
import requests
from datetime import datetime

# ===== ENTER YOUR API KEY BELOW =====
OPENROUTER_API_KEY = "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"  # Replace with your actual key from https://openrouter.ai/keys

# App UI
st.set_page_config(page_title="Sportify - AI Fitness Coach", layout="wide")
st.title("Sportify")
st.caption("Create your personalized training plan")

# User Inputs
with st.form("inputs"):
    col1, col2 = st.columns(2)
    with col1:
        sport = st.text_input("Sport", placeholder="e.g., Wheelchair Basketball", key="sport")
        equipment = st.text_input("Equipment Availability",
                                  placeholder="e.g., Dumbbells only, No equipment, Full gym access")
        difficulty = st.select_slider("Skill Level",
                                      ["Beginner", "Intermediate", "Advanced", "Professional"])

        # NEW: Training duration selector
        days = st.slider("Training Plan Duration (days)",
                         min_value=1, max_value=30, value=7,
                         help="The plan will progressively increase in difficulty")

    with col2:
        disability = st.text_input("Adaptations", placeholder="e.g., Amputee, Visual Impairment")
        culture = st.text_input("Cultural Needs", placeholder="e.g., Halal, Kosher")
        diet = st.text_input("Diet Plan", placeholder="e.g., Vegetarian, High-protein")

    generate_btn = st.form_submit_button("Generate Plan", type="primary")


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
        "max_tokens": 2000  # Increased for longer plans
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
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
        st.warning("Please add your OpenRouter API key in the code!")
    else:
        with st.spinner(f"🧠 Designing your {days}-day {sport} plan..."):
            prompt = f"""Create a {difficulty.lower()} {sport} training plan spanning {days} days with:
            - Physical adaptations: {disability if disability else "None"}
            - Available equipment: {equipment if equipment else "Basic bodyweight"}
            - Cultural/religious needs: {culture if culture else "None"}
            - Dietary preferences: {diet if diet else "Balanced diet"}

            Requirements:
            1. Progressive overload - intensity should increase gradually
            2. Include rest days as needed (approximately every 3-5 days)
            3. For each day, specify:
               - Warm-up (dynamic exercises)
               - Main workout (3-5 adapted exercises)
               - Cooldown (static stretches)
               - Duration estimate
            4. Equipment alternatives based on: {equipment}
            5. Safety precautions
            6. Nutrition recommendations matching: {diet if diet else "general fitness diet"}

            Format as markdown with:
            - Daily headers (Day 1, Day 2...)
            - Clear bullet points
            - Emoji icons for different sections (🏋️ for workout, 🧘 for cooldown, etc.)"""

            result = call_deepseek(prompt)

            if result:
                plan = result["choices"][0]["message"]["content"]
                st.subheader(f"Your {days}-Day {sport} Plan ({difficulty})")
                st.markdown(plan)

                st.download_button(
                    label="Save Plan",
                    data=plan,
                    file_name=f"{sport.replace(' ', '_')}_{days}day_plan.md",
                    mime="text/markdown"
                )
            else:
                st.error("Failed to generate plan. Check your API key and try again.")