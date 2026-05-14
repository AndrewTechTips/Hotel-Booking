import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from modules import SpaHotel, SecureCreditCard, ReservationTicket

# Ui config
st.set_page_config(
    page_title="Lux Booking Engine", layout="wide", initial_sidebar_state="collapsed"
)

st.markdown(
    """
<style>
    .stApp { background-color: #0d1117; }
    .hotel-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        margin-bottom: 20px;
        height: 280px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .status-available { color: #3fb950; font-weight: bold; font-size: 0.85em; }
    .status-booked { color: #f85149; font-weight: bold; font-size: 0.85em; }
    h3 { margin-bottom: 5px !important; color: #f0f6fc; }
    p { color: #8b949e; font-size: 0.9em; }
</style>
""",
    unsafe_allow_html=True,
)


# data loading, cached for performance
@st.cache_data
def load_data():
    df_hotels = pd.read_csv("data/hotels.csv", dtype={"id": str})
    df_cards = pd.read_csv("data/cards.csv", dtype=str).to_dict(orient="records")
    df_sec = pd.read_csv("data/card-security.csv", dtype=str)
    dict_security = dict(zip(df_sec.number, df_sec.password))

    return df_hotels, df_cards, dict_security
