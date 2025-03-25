import streamlit as st
import requests
import time
import os

# ===== ANIMATION SPEED CONTROLS =====
PROGRESS_SHIMMER_SPEED = "2s"  # Fixed missing time unit
PROGRESS_FILL_SPEED = 0.2

# Set page config
st.set_page_config(page_title="Sportify AI - Your AI Fitness Coach", layout="wide")

# Get environment variable - no dotenv needed
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Custom CSS with adjustable animation
st.markdown(f"""
<style>
    /* Cursor styles */
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] div[role="button"],
    div[role="listbox"] div,
    button {{
        cursor: pointer !important;
    }}

    /* Progress bar animation */
    .stProgress > div > div > div > div {{
        background-image: linear-gradient(
            to right,
            #4CAF50,
            #8BC34A,
            #4CAF50
        );
        background-size: 200% 100%;
        animation: progressAnimation {PROGRESS_SHIMMER_SPEED} linear infinite;
    }}

    @keyframes progressAnimation {{
        0% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
</style>
""", unsafe_allow_html=True)


# [REST OF YOUR TRANSLATIONS DICTIONARY REMAINS EXACTLY THE SAME...]

# [LANGUAGE SELECTION AND UI CODE REMAINS THE SAME...]

# API Call Function
def call_deepseek(prompt):
    if not OPENROUTER_API_KEY:
        st.error("API key not configured!")
        return None

    progress_bar = st.progress(0)
    progress_text = st.empty()
    progress_text.text(lang["loading_text"])

    try:
        # Initial progress
        for i in range(10, 31, 5):
            progress_bar.progress(i)
            time.sleep(PROGRESS_FILL_SPEED)

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

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=45
        )

        # [REST OF YOUR PROGRESS BAR CODE...]
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None
    finally:
        time.sleep(0.3)
        progress_bar.empty()
        progress_text.empty()

# [REST OF YOUR GENERATE PLAN CODE REMAINS THE SAME...]