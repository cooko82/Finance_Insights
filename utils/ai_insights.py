import requests
import pandas as pd
import ollama
import logging

#uses ollama locally refer to read me

def ai_insights(history_df, symbol, prompt=None):
  default_prompt = f"Give financial insights for {symbol} based on this data only: {history_df.tail().to_string()}"

  if prompt:
    final_prompt = prompt
  else:
    final_prompt = default_prompt 

  #create a client to instinate
  client = ollama.Client()
  try:
    res= client.generate(
      model="phi3", 
      prompt=final_prompt
      )
    
    insights = res.get("response", "Could not generate insights")
    return insights
  except Exception as e:
    logging.error(f"Ollama API call failed {e}")
    return "Error contacting the AI model soz"