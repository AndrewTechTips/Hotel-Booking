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


df_hotels, df_cards, dict_security = load_data()


# state management
if "page" not in st.session_state:
    st.session_state.page = "list"
if "selected_hotel" not in st.session_state:
    st.session_state.selected_hotel = None


# navigation logic
def go_to_booking(hotel_row):
    st.session_state.selected_hotel = hotel_row
    st.session_state.page = "booking"


def go_to_list():
    st.session_state.selected_hotel = None
    st.session_state.page = "list"


# page 1 , hotel view
if st.session_state.page == "list":
    st.title("🌌 Explore Destinations")
    st.markdown("Find and book the best luxury hotels around the world.")
    st.divider()

    # create a grid with 3 columns
    cols = st.columns(3)

    for index, row in df_hotels.iterrows():
        # distribute hotels across columns
        with cols[index % 3]:
            is_available = row["available"] == "yes"
            status_class = "status-available" if is_available else "status-booked"
            status_text = "● Available" if is_available else "● Fully Booked"

            # rendering the card
            st.markdown(
                f"""
            <div> class = "hotel-card">
                <div>
                    <h3>{row['name']}</h3>
                    <p>📍{row['city']}</p>
                    <p>👥Max Capacity: {row['capacity']} guests</p>
                    <span class ="{status_class}">{status_text}</span>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            # action button
            if is_available:
                st.button(
                    f"Select {row['name']}",
                    key=f"btn_{row['id']}",
                    on_click=go_to_booking(),
                    args=(row.to_dict(),),
                )
            else:
                st.button("Unavailable", key=f"btn_{row['id']}", disabled=True)

# page 2, booking details and payment
elif st.session_state.page == "booking":
    hotel_data = st.session_state.selected_hotel
