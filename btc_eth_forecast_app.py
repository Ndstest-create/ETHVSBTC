import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from ta.momentum import StochasticOscillator
from ta.trend import MACD
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(page_title="Crypto Multi-Asset Dashboard", layout="wide")
st.title("📊 Crypto Dashboard: วิเคราะห์ราคาคริปโตและอินดิเคเตอร์")

# Sidebar
crypto = st.sidebar.selectbox("เลือกเหรียญ", ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD"])
start_date = st.sidebar.date_input("จากวันที่", value=datetime(2021, 1, 1))
end_date = datetime.today().strftime('%Y-%m-%d')

# โหลดข้อมูล
@st.cache_data
def load_data(symbol, start, end):
    df = yf.download(symbol, start=start, end=end)
    df = df[['Close']]
    df.dropna(inplace=True)
    df.reset_index(inplace=True)
    return df

data = load_data(crypto, start_date, end_date)

# คำนวณ MACD
macd = MACD(close=data['Close'])
data['MACD'] = macd.macd()
data['MACD_Signal'] = macd.macd_signal()

# คำนวณ Stochastic Oscillator
stoch = StochasticOscillator(high=data['Close'], low=data['Close'], close=data['Close'])
data['Stoch_K'] = stoch.stoch()
data['Stoch_D'] = stoch.stoch_signal()

# พยากรณ์ราคาวันถัดไป
def forecast_price(df):
    df = df.copy()
    df['Day'] = np.arange(len(df)).reshape(-1, 1)
    X = df['Day'].values.resha
