# ----------------- Imports ----------------------
import os
from typing import TypedDict

from dotenv import load_dotenv
from pydantic import BaseModel

from langgraph.graph import StateGraph, START, END
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.openweathermap import OpenWeatherMapQueryRun
from langchain_nvidia_ai_endpoints import ChatNVIDIA

# ------------- Setup ------------------------

load_dotenv()

if not os.getenv("OPENWEATHERMAP_API_KEY"):
    raise EnvironmentError("Missing OPENWEATHERMAP_API_KEY in .env")

if not os.getenv("NVIDIA_API_KEY"):
    raise EnvironmentError("Missing NVIDIA_API_KEY in .env")

# ------------- Tools -------------------------------
weather_service = OpenWeatherMapQueryRun()
web_search = DuckDuckGoSearchRun()

# ---------------------- LLM ----------------------------

llm = ChatNVIDIA(
    model="meta/llama-3.1-8b-instruct",
    temperature=0.0,
    max_completion_tokens=512,
)

# -------------------- Structured output -----------------

class LocationSuggestionResult(BaseModel):
    suggestion: str


suggestion_llm = llm.with_structured_output(LocationSuggestionResult)


# -----------------------State ---------------------
class WeatherAgentState(TypedDict, total=False):
    user_input: str
    detected_location: str
    is_valid_location: bool
    weather_data: str
    suggestion: str
    final_response: str


# --------------- Defining Nodes  ------------------------

def extract_location(state: WeatherAgentState) -> dict:
    prompt = f"""
Identify the location from this weather request.

Return:
- Only location name
- No explanation
- If missing, return NONE

User request:
{state['user_input']}
"""

    response = llm.invoke(prompt)
    location = response.content.strip()

    if location.upper() == "NONE":
        return {
            "final_response": "Please enter a valid city or location.",
            "is_valid_location": False,
        }

    # We have a candidate; actual validation will happen in validate_location.
    return {
        "detected_location": location,
        "is_valid_location": True,
    }


def validate_location(state: WeatherAgentState) -> dict:
    """Fast heuristic validation (no LLM call)."""
    location = state.get("detected_location", "")

    if not location:
        return {"is_valid_location": False}

    # Keep the query tight for speed.
    search_result = web_search.invoke(f"{location} city")

    if not search_result:
        return {"is_valid_location": False}

    text = str(search_result).strip().lower()
    evidence = any(
        token in text
        for token in ["city", "country", "population", "weather", "located", "capital"]
    )

    return {"is_valid_location": evidence or len(text) > 80}


def route_location(state: WeatherAgentState) -> str:
    return "fetch_weather" if state.get("is_valid_location") else "suggest_location"


def suggest_location(state: WeatherAgentState) -> dict:
    prompt = f"""
The location may be wrong or misspelled.

User request:
{state.get('user_input', '')}

Detected location:
{state.get('detected_location', '')}

Suggest the most likely real location.

Rules:
- Return one location only
- No explanation
- If unsure, return UNKNOWN
"""

    result = suggestion_llm.invoke(prompt)
    suggestion = result.suggestion.strip()

    if not suggestion or suggestion.upper() == "UNKNOWN":
        return {
            "final_response": "I couldn't verify that location. Please try again.",
            "suggestion": "",
        }

    return {
        "suggestion": suggestion,
        "final_response": f"I couldn't verify that location. Did you mean: {suggestion}?",
    }


def fetch_weather(state: WeatherAgentState) -> dict:
    try:
        weather_data = weather_service.invoke(state["detected_location"])

        if not weather_data:
            return {"final_response": "Weather data unavailable."}

        return {"weather_data": weather_data}

    except Exception:
        return {"final_response": "Unable to retrieve weather right now."}


def final_response_node(state: WeatherAgentState) -> dict:
    weather_report = state.get("weather_data", "").strip()

    if not weather_report:
        return {
            "final_response": "I couldn’t retrieve the weather details right now."
        }

    prompt = f"""
Write a natural, friendly weather update for the user.

Keep it clear and practical.

Weather report:
{weather_report}
"""

    final_response = llm.invoke(prompt)

    return {
        "final_response": final_response.content.strip()
    }


# -------------------- Graph ------------------------

builder = StateGraph(WeatherAgentState)

builder.add_node("extract_location", extract_location)
builder.add_node("validate_location", validate_location)
builder.add_node("suggest_location", suggest_location)
builder.add_node("fetch_weather", fetch_weather)
builder.add_node("final_response_node", final_response_node)


builder.add_edge(START, "extract_location")
builder.add_edge("extract_location", "validate_location")

builder.add_conditional_edges(
    "validate_location",
    route_location,
    {
        "fetch_weather": "fetch_weather",
        "suggest_location": "suggest_location",
    },
)

builder.add_edge("fetch_weather", "final_response_node")
builder.add_edge("suggest_location", END)
builder.add_edge("final_response_node", END)

weather_agent = builder.compile()

