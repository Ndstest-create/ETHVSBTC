import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime

# Title
st.title("🔮 พยากรณ์และเปรียบเทียบราคา Bitcoin และ Ethereum")

# Load historical data
@st.cache_data
def load_data(symbol):
    data = yf.download(symbol, start="2021-01-01", end=datetime.today().strftime("%Y-%m-%d"))
    data = data[['Close']].copy()
    data.reset_index(inplace=True)
    return data

btc_data = load_data('BTC-USD')
eth_data = load_data('ETH-USD')

# Plot prices
st.subheader("📈 เปรียบเทียบราคาย้อนหลัง (2021 - ปัจจุบัน)")
fig1, ax1 = plt.subplots()
ax1.plot(btc_data['Date'], btc_data['Close'], label='Bitcoin (BTC)')
ax1.plot(eth_data['Date'], eth_data['Close'], label='Ethereum (ETH)')
ax1.set_ylabel("USD")
ax1.set_title("BTC vs ETH")
ax1.legend()
st.pyplot(fig1)

# Forecasting with Linear Regression
st.subheader("🤖 พยากรณ์ราคาวันถัดไปด้วย Linear Regression")

def forecast_price(data, name):
    df = data.copy()
    df['Days'] = (df['Date'] - df['Date'].min()).dt.days
    X = df[['Days']]
    y = df['Close']

    model = LinearRegression()
    model.fit(X, y)

    next_day = [[X['Days'].max() + 1]]
    predicted_price = model.predict(next_day)[0]

    st.write(f"📌 พยากรณ์ราคา {name} ในวันถัดไป: **${predicted_price:,.2f}**")

    # Plot fit line
    fig2, ax2 = plt.subplots()
    ax2.scatter(X, y, alpha=0.3, label='Historical')
    ax2.plot(X, model.predict(X), color='red', label='Linear Fit')
    ax2.set_xlabel('Days since 2021-01-01')
    ax2.set_ylabel('Price (USD)')
    ax2.set_title(f'{name} Price Trend')
    ax2.legend()
    st.pyplot(fig2)

forecast_price(btc_data, "Bitcoin (BTC)")
forecast_price(eth_data, "Ethereum (ETH)")
