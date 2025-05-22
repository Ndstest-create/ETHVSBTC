import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import ta

st.set_page_config(page_title="Crypto Dashboard", layout="wide")
st.title("📈 Crypto Investment Dashboard")

# Sidebar
crypto = st.sidebar.selectbox("เลือกเหรียญ", ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD"])
start_date = st.sidebar.date_input("จากวันที่", value=datetime(2021, 1, 1))
end_date = datetime.today().strftime('%Y-%m-%d')

# Load data
@st.cache_data
def load_data(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    data = data[['Close', 'Volume']]
    data.dropna(inplace=True)
    return data

data = load_data(crypto, start_date, end_date)
data['SMA20'] = data['Close'].rolling(20).mean()
data['SMA50'] = data['Close'].rolling(50).mean()

# Plot
st.subheader(f"📊 ราคา {crypto} พร้อม SMA(20, 50)")
fig, ax = plt.subplots(figsize=(12,6))
ax.plot(data['Close'], label='Close Price', color='blue')
ax.plot(data['SMA20'], label='SMA 20', color='green', linestyle='--')
ax.plot(data['SMA50'], label='SMA 50', color='red', linestyle='--')
ax.set_title(f"{crypto} Price Chart")
ax.set_ylabel("USD")
ax.legend()
st.pyplot(fig)

st.subheader("🔎 ข้อมูลล่าสุด")
st.dataframe(data.tail())

