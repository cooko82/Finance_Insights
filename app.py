import streamlit as st
import base64
import utils.data_fetcher
import pandas as pd

from utils.charts import price_chart
from utils.ai_insights import ai_insights

#rn using ollama for insights may change later

fetcher = utils.data_fetcher
st.set_page_config(page_title="Stock Insights Dashboard", layout="wide")
st.title("Stock Insights Dashboard")

#intialise the session state
if 'run' not in st.session_state:
  st.session_state.run = False
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'initial_insights' not in st.session_state:
    st.session_state.initial_insights = "No initial analysis performed yet."
if 'insights_ticker' not in st.session_state: # Use this to prevent re-running the LLM
    st.session_state.insights_ticker = ""

ticker = "Enter here" #
#sidebar
st.sidebar.header("Choose what you want to see: ")
symbol = st.sidebar.text_input("Stock Symbol", ticker)
period = st.sidebar.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"])

#add button for content
if st.sidebar.button("Fetch and analyse data"):
  #when button clicked, make state run and stored ticker and period
  st.session_state.run = True
  st.session_state.symbol = symbol #sotre the value from the sidebar
  st.session_state.period = period


if st.session_state.get("run"):

  ticker = st.session_state.symbol
  period = st.session_state.period

  #tab layout
  tab1, tab2, tab3, tab4 = st.tabs(["📈 Price", "ℹ️ Info", "🤖 AI Insights", "📰 News"])

  #price tab
  with tab1:
    st.subheader(f"{ticker} - Price Chart")
    his_df = fetcher.fetch_history(ticker, period)

    if his_df.empty ==False:
      img_b64 = price_chart(his_df, ticker)
      chart_image = base64.b64decode(img_b64)
      st.image(chart_image)

      #live price
      price = fetcher.fetch_live_price(ticker)
      if price:
        st.metric("Live price: ", f"${price:.2f}")
    else:
      st.error("No price data found at the moment, check again later")

    #info tab
    with tab2:
      st.subheader(f"{ticker} - Company info")
      info = fetcher.fetch_info(ticker)
      #st.write(info) #this prints it in standard form
      
      # Check if the 'info' dictionary is available
      # if info: # Assuming 'info' has been fetched successfully
          
      # --- 1. Key Business Summary ---
      st.header("📚 Overview")
      st.markdown(f"**Industry:** {info.get('industry', 'N/A')} ({info.get('sector', 'N/A')})")
      st.markdown(f"**Employees:** {info.get('fullTimeEmployees', 'N/A'):,}")
      
      # Use an expander for the long business summary
      with st.expander("Read Full Business Summary"):
          st.write(info.get('longBusinessSummary', 'No summary available.'))
          
      st.markdown("---")

      # --- 2. Contact and Location ---
      st.header("📍 Contact & Location")
      
      # Use columns for side-by-side display
      col1, col2 = st.columns(2)
      
      with col1:
          st.markdown(f"**Website:** [{info.get('website', 'N/A')}]({info.get('website', '')})")
          st.markdown(f"**Phone:** {info.get('phone', 'N/A')}")
          
      with col2:
          address = f"{info.get('address1', '')}, {info.get('city', '')}, {info.get('state', '')} {info.get('zip', '')}, {info.get('country', '')}"
          st.markdown(f"**Address:** {address}")

      st.markdown("---")
      
      # --- 3. Key Officers (Handling the complex list) ---
      st.header("🧑‍💼 Key Leadership")
      
      officers = info.get("companyOfficers", [])
      
      if officers:
          # Create a DataFrame for officers to display as a clean table
          officer_data = []
          for officer in officers:
              officer_data.append({
                  "Name": officer.get("name", "N/A"),
                  "Title": officer.get("title", "N/A"),
                  "Age": officer.get("age", "N/A")
              })
              # Limit to the first two officers for brevity in the table
              if len(officer_data) >= 2:
                  break
          
          # Display the formatted table
          st.dataframe(pd.DataFrame(officer_data), hide_index=True, use_container_width=True)
          
      else:
          st.write("No officer data available.")

    
    #ai tab
    with tab3:
      st.subheader(f"{ticker} - AI generated insights")
      if his_df.empty == False:
        ai = ai_insights(his_df, ticker)
        st.write(ai)
      else:
        st.write("Cannot generate insights right now try again later")
      st.markdown("---") 

    # interactive Q&A Box 
      
      st.markdown("### Ask the AI a follow-up question:")
      
      # dsplay the previous chat messages 
      # for message in st.session_state.messages:
      #     with st.chat_message(message["role"]):
      #         st.markdown(message["content"])

      # 2. Use st.chat_input to capture the user's new question
      prompt = st.chat_input("Ask about valuation, risks, or performance...")

      if prompt:
          # Add user's question to chat history
          st.session_state.messages.append({"role": "user", "content": prompt})
          
          # Display the user's question immediately
          with st.chat_message("user"):
              st.markdown(prompt)

          # 3. Call the AI model with the new question
          with st.chat_message("assistant"):
              with st.spinner("Analyzing question..."):
                  # Use a specific prompt that gives context to the LLM 
                  context_prompt = (
                      f"You are a financial analyst. Answer the user's question based on the previous insights and the following context: "
                      f"Stock: {ticker}. Initial Insight: {st.session_state.initial_insights}. "
                      f"User Question: {prompt}"
                  )
                  
                  # Assuming ai_insights function can be used for chat or you define a new one
                  follow_up_answer = ai_insights(his_df, ticker, prompt=context_prompt)
                  
                  st.markdown(follow_up_answer)
                  
                  # Add AI's answer to chat history
                  st.session_state.messages.append({"role": "assistant", "content": follow_up_answer})
      
    #news tab
    with tab4:
      st.subheader(f"{ticker} - News")
      news_dict = fetcher.fetch_news(ticker)

      if len(news_dict[f"{ticker} news"]) > 0:
        st.write("News exists")
      
      else:
        st.write("No news available right now :(")

