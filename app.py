
import streamlit as st
import requests
import json

# Page Configuration
st.set_page_config(
    page_title="ScamRadar AI",
    page_icon="🛡️",
    layout="centered"
)

# Application Title
st.title("🛡️ ScamRadar AI")
st.subheader("AI-Powered Scam Message Detection System")

st.write(
    "Analyze suspicious SMS, emails, job offers "
    "and online messages using Artificial Intelligence."
)

st.divider()

# User Input
message = st.text_area(
    "Enter your suspicious message:",
    placeholder="Paste your SMS, email or job offer here...",
    height=180
)

# Model Configuration
MODEL = "gemma3:1b"
OLLAMA_URL = "http://localhost:11434/api/chat"

# Investigation Function
def investigate_message(message):

    prompt = f"""
    Analyze this message for possible scam indicators.

    Message: {message}

    Return ONLY valid JSON with these fields:
    {{
        "concern_level": "Low Concern / Medium Concern / High Concern",
        "message_type": "SMS / Email / Job Offer / Other",
        "summary": "Short explanation",
        "warning_signs": ["warning 1", "warning 2"],
        "recommended_actions": ["action 1", "action 2"],
        "limitations": "Explain limitations"
    }}

    Do not assume every message is a scam.
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "format": "json"
        },
        timeout=120
    )

    response.raise_for_status()

    result = response.json()
    return json.loads(result["message"]["content"])


# Investigation Button
if st.button("🔍 Investigate Message", use_container_width=True):

    if not message.strip():
        st.warning("Please enter a message first.")

    else:
        try:
            with st.spinner("Analyzing message..."):
                report = investigate_message(message)

            st.success("Investigation Completed!")

            st.subheader("Investigation Report")

            concern = report.get("concern_level", "Unknown")

            st.markdown(f"### Concern Level: {concern}")

            st.write("**Message Type:**", report.get("message_type", "Unknown"))

            st.write("**Summary:**", report.get("summary", ""))

            st.write("### Warning Signs")
            for sign in report.get("warning_signs", []):
                st.write("⚠️", sign)

            st.write("### Recommended Safety Actions")
            for action in report.get("recommended_actions", []):
                st.write("✅", action)

            st.write("### Limitations")
            st.info(report.get("limitations", ""))

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to Ollama. Make sure Ollama is running.")

        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")

        except (ValueError, KeyError):
            st.error("Invalid AI response. Please try again.")

        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {e}")

st.divider()

st.caption("ScamRadar AI | AI-generated assessments are not guaranteed scam verdicts.")
          
