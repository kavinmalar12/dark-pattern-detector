import streamlit as st
import requests
from bs4 import BeautifulSoup

# Dark pattern keywords
patterns = {
    "urgency": ["hurry", "only few left", "limited time", "ends soon"],
    "scarcity": ["limited stock", "out of stock soon"],
    "pressure": ["buy now", "order now", "last chance"],
    "hidden": ["extra charges", "terms apply"]
}

def analyze_text(text):
    score = 0
    found = []
    explanations = []

    text = text.lower()

    for category, words in patterns.items():
        for word in words:
            if word in text:
                score += 15
                found.append(word)

                if category == "urgency":
                    explanations.append(f"Uses urgency like '{word}' to push quick action.")
                elif category == "scarcity":
                    explanations.append(f"Creates scarcity using '{word}'.")
                elif category == "pressure":
                    explanations.append(f"Applies pressure with '{word}'.")
                elif category == "hidden":
                    explanations.append(f"Possible hidden info using '{word}'.")

    score = min(score, 100)

    if score > 60:
        level = "High Manipulation"
    elif score > 30:
        level = "Moderate Manipulation"
    else:
        level = "Low Manipulation"

    return score, level, found, explanations


# UI
st.title("Dark Pattern Detector")

url = st.text_input("Enter product URL")

if st.button("Analyze"):
    if url:
        try:
            if not url.startswith("http"):
                url = "http://" + url

            headers = {"User-Agent": "Mozilla/5.0"}

            st.write("Fetching website...")

            response = requests.get(url, headers=headers, timeout=5)

            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text()

            score, level, found, explanations = analyze_text(text)

            st.subheader(f"Score: {score}/100")
            st.write(level)

            st.subheader("Detected Patterns")
            for f in found:
                st.write("-", f)

            st.subheader("Explanation")
            for e in explanations:
                st.write("-", e)

        except Exception as e:
            st.error("Error fetching website")
    else:
        st.warning("Please enter a URL")
