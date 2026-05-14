import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from modules import SpaHotel, SecureCreditCard, ReservationTicket

st.set_page_config(
    page_title="Lux Booking Engine", layout="wide", initial_sidebar_state="collapsed"
)
