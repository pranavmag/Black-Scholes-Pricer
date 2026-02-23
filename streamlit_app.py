import streamlit as st
import requests

st.title("Black-Scholes Option Pricer")

with st.sidebar:
    st.header(" Option Parameters")
    current_price = st.number_input("Current Asset Price)", value=100.0)
    strike_price = st.number_input("Strike Price", value=100.0)
    time = st.slider("Time to Expiration (Years)", 0.1, 5.0, 1.0)
    rate = st.slider("Risk-Free Interest Rate", 0.01, 0.20, 0.05)
    vol = st.slider("Volatility", 0.1, 1.0, 0.2)

if st.button("Calculate"):
    payload = {
        "current_asset_price": current_price,
        "strike_price": strike_price,
        "time_to_expiration": time,
        "risk_free_interest_rate": rate,
        "volatility": vol,
    }

    response = requests.post("http://127.0.0.1:8000/calculate-options", json=payload)

    if response.status_code == 200:
        data = response.json()
        st.success(f"Call Price: ${data['call_price']}")
        st.success(f"Put Price: ${data['put_price']}")

