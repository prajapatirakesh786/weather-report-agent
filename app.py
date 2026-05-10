# ---------------- Imports --------------------------------------------
import streamlit as st
from weather_agent import weather_agent


# ------------------ Page setup -----------------------

st.set_page_config(page_title="Weather Agent", page_icon="🌤")

st.title("🌤 Weather Report Agent")
st.write("Enter a city name.")

# ------------------- Input ---------------------------------------------


user_input = st.text_input(
    "Enter location:",
    placeholder="Jaipur, Mumbai weather, Tokyo..."
)

# ------------------------ Weather Button --------------------------------

if st.button("Get Weather"):

    if not user_input.strip():
        st.warning("Please enter a location.")

    else:
        with st.spinner("Checking weather..."):

            result = weather_agent.invoke(
                {
                    "user_input": user_input,
                    "weather_data": "",
                    "suggestion": "",
                    "error": None,
                }
            )

        suggestion = result.get("suggestion", "")
        final_response = result.get("final_response", "")

        # Wrong / unclear location
        if suggestion:
            st.warning(final_response)

            corrected_result = weather_agent.invoke(
                {
                    "user_input": f"What is the weather in {suggestion}?",
                    "weather_data": "",
                    "suggestion": "",
                    "error": None,
                }
            )

            st.info("Showing weather for suggested location:")
            st.success(corrected_result.get("final_response", ""))

        # Correct location
        else:
            st.success(final_response)