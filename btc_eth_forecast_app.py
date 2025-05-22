import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime

st.set_page_config(page_title="BTC vs ETH Forecast", layout="wide")
st.title("📊 วิเคราะห์และพยากรณ์ราคา Bitcoin (BTC) และ Ethereum (ETH) เทียบกับ M2")

@st.cache_data
def load_data(symbol):
    data = yf.download(symbol, start="2021-01-01", end=datetime.today().strftime("%Y-%m-%d"))
    data = data[['Close']].copy()
    data.reset_index(inplace=True)
    return data

btc_data = load_data('BTC-USD')
eth_data = load_data('ETH-USD')
m2_data = load_data('M2SL')  # ปริมาณเงิน M2

st.subheader("📈 ราคาย้อนหลัง BTC, ETH และปริมาณเงิน M2")

fig, ax1 = plt.subplots(figsize=(12, 5))

ax1.plot(btc_data['Date'], btc_data['Close'], label='Bitcoin (BTC)', color='orange')
ax1.plot(eth_data['Date'], eth_data['Close'], label='Ethereum (ETH)', color='blue')
ax1.set_ylabel('Price (USD)', color='black')
ax1.tick_params(axis='y', labelcolor='black')

ax2 = ax1.twinx()
ax2.plot(m2_data['Date'], m2_data['Close'], label='M2 Supply', color='green', linestyle='--')
ax2.set_ylabel('M2 Supply (Billions USD)', color='green')
ax2.tick_params(axis='y', labelcolor='green')

fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.85))
ax1.set_title('BTC & ETH Prices vs M2 Supply')
st.pyplot(fig)

def forecast_price(data, name):
    df = data.copy()
    df['Days'] = (df['Date'] - df['Date'].min()).dt.days
    X = df[['Days']]
    y = df['Close']

    model = LinearRegression()
    model.fit(X, y)

    next_day = [[X['Days'].max() + 1]]
    predicted_price = float(model.predict(next_day)[0])

    st.write(f"📌 พยากรณ์รา
