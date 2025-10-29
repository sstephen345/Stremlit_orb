import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz, random

st.set_page_config(page_title="Streamlit ORB Starter", layout="wide")
IST = pytz.timezone("Asia/Kolkata")

# ── header
st.title("📈 Streamlit ORB Starter")
st.caption(f"IST: **{datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S')}**")

# ── controls
c1, c2, c3 = st.columns(3)
with c1:
    symbol = st.text_input("Symbol", "NIFTY")
with c2:
    strategy = st.selectbox("Strategy", ["Standard ORB", "Reversed ORB"])
with c3:
    use_filters = st.toggle("Filters (RSI>75, EMA↑, ATR↑)", value=False)

st.divider()

# ── demo data + simple ORB simulation (no broker yet)
np.random.seed(0)
start = datetime.now(IST).replace(hour=9, minute=15, second=0, microsecond=0)
times = pd.date_range(start, periods=25, freq="15min")
base = 24000.0
close = base + np.cumsum(np.random.uniform(-10, 10, len(times)))
high  = close + np.random.uniform(2, 6, len(times))
low   = close - np.random.uniform(2, 6, len(times))
openp = np.r_[close[0], close[:-1]]

df = pd.DataFrame({"Time": times, "Open": openp, "High": high, "Low": low, "Close": close})

# ORB = first candle 9:15–9:30
orb_high, orb_low = df.iloc[0]["High"], df.iloc[0]["Low"]

# demo “entries” after 9:30
entries = []
for i, row in df.iloc[1:].iterrows():
    if row["Close"] > orb_high:
        entries.append(("BUY", i, row["Close"]))
        break
    if row["Close"] < orb_low:
        entries.append(("SELL", i, row["Close"]))
        break

st.subheader("Preview (demo)")
colA, colB = st.columns([2,1])
with colA:
    st.dataframe(df, use_container_width=True)
with colB:
    st.metric("ORB High", round(float(orb_high),2))
    st.metric("ORB Low",  round(float(orb_low),2))
    if entries:
        side, idx, price = entries[0]
        st.success(f"First breakout → {side} at {df.iloc[idx]['Time'].strftime('%H:%M')} @ {round(float(price),2)}")
    else:
        st.info("No breakout in demo data.")

st.caption("✅ App runs. Next: add real indicators, live LTP, and Angel One wiring.")
