# 📈 Stock Insights Dashboard: Technical Overview

This repository contains a Streamlit application that provides stock insights and analysis. It uses the yfinance API to fetch historical and real-time price data, as well as news articles related to a particular stock. The application also utilizes the Ollama API to generate AI-generated insights based on the historical data.

## Key Features

* **Dynamic UI with Streamlit:** Built using the **Streamlit** Python framework, providing a responsive and interactive user interface with multi-tab navigation. Custom CSS is used to enhance the appearance and spacing of the navigation tabs.
* **Time-Series Visualization:** Generates and displays a historical **price chart** (OHLC data) for a user-specified stock ticker and time period.
* **Real-Time Metrics:** Fetches and displays the **live price** and critical financial metadata (e.g., industry, sector, employee count, leadership).
* **AI-Powered Contextual Analysis:** Integrates a local **Large Language Model (LLM)** via the Ollama API to generate in-depth, context-aware financial insights based on the fetched historical data.
* **Interactive Q&A:** Implements a **chat interface** (`st.chat_input`) allowing users to ask **follow-up questions** to the LLM, grounding the responses in the initial analysis and stock context using session state (`st.session_state`) for conversation history.

---
## Example of what it looks like

### Generated chart after inputing the stock
<img width="1281" height="692" alt="image" src="https://github.com/user-attachments/assets/881215ea-a436-4e7a-971f-f678752d0b9f" />

### Generated company info
<img width="1334" height="722" alt="image" src="https://github.com/user-attachments/assets/6af50bc9-89e2-4af8-bc94-ae3e8cdb8386" />

### Ai insights
<img width="1466" height="706" alt="image" src="https://github.com/user-attachments/assets/8ea8475d-61a5-4f3e-838a-fd3e52e81070" />
ask follow-up questions to LLM
<img width="1412" height="707" alt="image" src="https://github.com/user-attachments/assets/d641a59b-a406-4cd6-ab43-da7f070cd3ef" />



---

## Technical Stack and Architecture

This project leverages a modern Python data science stack with a focus on local LLM deployment.

### 1. Core Framework
* **Streamlit:** Serves as the web application layer, handling application flow, state management, and all front-end rendering.

### 2. Data Acquisition (APIs)
* **`yfinance`:** Used as the primary financial data connector.
    * **Historical Data:** Fetches pandas DataFrames containing Open, High, Low, Close, and Volume data.
    * **Metadata & News:** Retrieves essential corporate information and news headlines.

### 3. AI/NLP Engine
* **Ollama API (Local Host):** Manages and runs the local language model (e.g., **Phi-3**).
    * **Communication:** Utilizes the official **`ollama-python`** client library for robust interaction.
    * **Prompt Engineering:** The LLM prompt is dynamically constructed, including serialized DataFrame data (`DataFrame.to_string()`) and the user's specific question to ensure contextual accuracy.

### 4. Visualization & Utilities
* **Matplotlib:** Used for generating and rendering the historical price chart. The resulting image is converted to a **Base64-encoded PNG string** via `io.BytesIO` before being displayed by Streamlit's `st.image()`.
* **Pandas:** Essential for data manipulation, handling time-series data, and creating clean tabular outputs (e.g., for company officer lists).

---

To run the application, you need to create a virtual environment and install the required dependencies. You can do this by running the following commands:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
After installing the dependencies, you need to install the Ollama model by running the following commands:

```bash
ollama pull phi3
```
You can then start the Ollama server by running the following command:

```bash
brew services start ollama
ollama run phi3
```

clone repo then run
```bash
streamlit run app.py
```