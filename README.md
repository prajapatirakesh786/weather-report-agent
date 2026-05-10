# 🌤 Weather Report Agent

A simple AI-powered weather assistant built with **Streamlit**, **LangGraph**, **LangChain**, **NVIDIA NIM**, and **OpenWeatherMap**.

This app lets users enter a city or natural language weather query, validates the location, suggests corrections for misspelled places, fetches live weather data, and displays results through a clean Streamlit UI.

---

# Features

- Natural language weather requests  
- City/location extraction using LLM  
- Real-world location validation  
- Misspelled location suggestions  
- Live weather retrieval  
- Streamlit web interface  
- Clean LangGraph workflow  

---

# Demo Examples

## Valid Input
```bash
Jaipur
Mumbai weather
What's the weather in Tokyo?
```

## Invalid Input
```bash
Jaidur
Mumbbai
Delhii
```

---

# Example Output

## Correct Location
```bash
It's currently hot and hazy in Jaipur with temperatures around 37°C...
```

## Wrong Location
```bash
I couldn't verify that location. Did you mean: Jaipur?
```

---

# Project Structure

```
Weather Report Agent/
│
├── app.py                 # Streamlit frontend
├── weather_agent.py       # LangGraph backend
├── requirements.txt       # Dependencies
├── .env                   # API keys
└── README.md              # Documentation
```


---

# Installation Guide

## Step 1: Clone the Repository

```bash
git clone <your_repo_url>
cd Weather\ Report\ Agent

```

---

## Step 2: Create Virtual Environment

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```
---

# Step 4: Add API Keys

Create a `.env` file in your root folder:

```env
NVIDIA_API_KEY=your_nvidia_api_key
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
```

---

# API Key Setup

## NVIDIA API Key
Used by the LLM for:
- extracting the location from the user message
- suggesting the correct location when the input is unclear
- writing the final weather response

Get it from:
https://build.nvidia.com/


---

## OpenWeatherMap API Key
Used for live weather data.

Get it from:  
https://openweathermap.org/api

---

# Running the App

## Start Streamlit UI

```bash
streamlit run app.py
```

---

# How to Use

1. Enter a city name or weather question  
2. Click **Get Weather**  
3. If valid → Weather appears  
4. If invalid → Suggestion appears automatically  

---

# Streamlit Workflow

```bash
User Input
   ↓
Click Get Weather
   ↓
Extract Location
   ↓
Validate Location
   ↓
 ┌─────────────────┐
Valid            Invalid
 ↓                ↓
Fetch Weather    Suggest Location
 ↓                ↓
Show Result      Show Suggestion
```

---

# LangGraph Backend Flow

```bash
START
  ↓
extract_location
  ↓
validate_location
  ↓
┌──────────────────────┐
│ if valid:             │
│   fetch_weather      │
│ else:                 │
│   suggest_location   │
└──────────────────────┘
  ↓                    ↓
final_response_node    END
  ↓
END
```


---

# Technologies Used

## Streamlit
Frontend UI

## LangGraph
Workflow orchestration

## LangChain
Tool integration

## NVIDIA (ChatNVIDIA)
LLM used for reasoning and generating responses


## DuckDuckGo Search
Location validation

## OpenWeatherMap
Weather data source

---

# Common Commands

## Reinstall Dependencies
```bash
pip install --upgrade -r requirements.txt
```

## Freeze Installed Packages
```bash
pip freeze > requirements.txt
```

---

# Troubleshooting

## Missing NVIDIA API Key
```bash
Missing NVIDIA_API_KEY in .env
```

### Fix:
Add your key to `.env`

---

## Missing OpenWeatherMap API Key
```bash
Missing OPENWEATHERMAP_API_KEY in .env
```

### Fix:
Add your key to `.env`

---

## Streamlit Not Found
```bash
streamlit: command not found
```

### Fix:
```bash
pip install streamlit
```

---

# Future Improvements

- 7-day forecast  
- Weather icons  
- Voice input  
- GPS auto-location  
- Mobile-friendly UI  
- Multi-language support  

---

# License

MIT License

---
