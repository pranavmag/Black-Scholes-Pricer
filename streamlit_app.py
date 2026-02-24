import streamlit as st
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

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
    heatmap_response = requests.post("http://127.0.0.1:8000/calculate-heatmap", json=payload)

    if response.status_code == 200 and heatmap_response.status_code == 200:
        st.session_state["pricing_data"] = response.json()
        st.session_state["heatmap_data"] = heatmap_response.json()

if "pricing_data" in st.session_state and "heatmap_data" in st.session_state:

    data = st.session_state["pricing_data"]
    heatmap_data = st.session_state["heatmap_data"]

    st.success(f"Call Price: ${data['call_price']}")
    st.success(f"Put Price: ${data['put_price']}")

    option_type = st.radio("Select Option Type", ["Call", "Put"])

    call_grid = np.array(heatmap_data['call_grid'])
    put_grid = np.array(heatmap_data['put_grid'])
    spot_prices = [round(x, 2) for x in heatmap_data['spot_prices']]
    volatilities = [round(x, 2) for x in heatmap_data['volatilities']]

    selected_grid = call_grid if option_type == "Call" else put_grid

    st.subheader(f"{option_type} Option Price Heatmap")
    st.write(f"Visualizing how the {option_type} price changes when Asset Price and Volatility are shocked.")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(
        selected_grid,
        xticklabels=spot_prices,
        yticklabels=volatilities,
        annot=True,
        fmt=".2f",
        cmap="RdYlGn",
        ax=ax
    )
    ax.set_xlabel("Asset Price")
    ax.set_ylabel("Volatility")
    ax.invert_yaxis()

    st.pyplot(fig)
