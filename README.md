This repository contains a Streamlit application that provides stock insights and analysis. It uses the yfinance API to fetch historical and real-time price data, as well as news articles related to a particular stock. The application also utilizes the Ollama API to generate AI-generated insights based on the historical data.



I. Application Architecture and Stack
Platform: Streamlit (Python web framework) for rapid development of the interactive user interface (UI) and server-side logic.

Execution Model: Client-server architecture where the Python backend (server) runs the Streamlit script, and the frontend (client) communicates with it via WebSockets for persistent, bi-directional updates. Application state is managed using st.session_state.

Data Layer: Relies on third-party financial APIs for data acquisition.

AI/NLP Layer: Integrates a local, self-hosted Language Model (LLM) via the Ollama API for context-aware analysis.

II. Data Acquisition and Processing
Historical Market Data:

Source: yfinance library (unofficial client for Yahoo Finance).

Data Retrieval: Fetches historical OHLC (Open, High, Low, Close) price data, adjusted close prices, and volume for a specified stock ticker.

Input Parameters: User-defined stock ticker symbol (e.g., AAPL, GOOGL) and a time period (e.g., 1y, 3mo, or custom date range).

Real-Time Data:

Retrieves the current price, daily change, and market status. Note: Streamlit updates typically require a manual rerun or time-based refresh mechanism (e.g., st.empty() or custom polling logic) to simulate "real-time" updates.

News Articles:

Source: yfinance metadata functionalities.

Data Structure: Fetches a list of recent, relevant news articles, typically including fields like title, publisher, and link.

III. User Interface (UI) and Visualization
Input Widgets: Utilizes Streamlit widgets such as st.text_input for the stock symbol and st.selectbox or st.date_input for the time period selection.

Primary Visualization: Displays the historical price data as a time-series chart (e.g., a Line Chart or Candlestick chart) using libraries such as Plotly Express or Altair via Streamlit's native charting functions (st.line_chart, st.plotly_chart).

Information Display: Uses Streamlit containers (st.container), columns (st.columns), and layout functions to structure the data (e.g., displaying current price metrics using st.metric).

News Display: Presents news articles in a structured format, possibly using st.dataframe or custom Markdown formatting (st.markdown) for readability.

IV. AI-Powered Analysis and Insights
LLM Integration: Communicates with the Ollama API endpoint (typically running locally on http://localhost:11434) via HTTP POST requests to generate text.

Contextual Prompting: The prompt sent to the LLM is dynamically constructed. It includes:

The user's query (the question about the stock).

Grounding Data: A serialized segment of the historical price data (e.g., recent closing prices, volume, and derived technical indicators) to provide context for the LLM's response.

System Instructions: Directives defining the LLM's persona (e.g., "Act as a financial analyst") and the required output format.

Output: The LLM's response provides AI-generated insights and analysis based on the provided historical data context.

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
ollama run phi3
```
