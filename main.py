import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from modules import SpaHotel, SecureCreditCard, ReservationTicket, ticket

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
            <div class="hotel-card">
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
                    on_click=go_to_booking,
                    args=(row.to_dict(),),
                )
            else:
                st.button("Unavailable", key=f"btn_{row['id']}", disabled=True)

# page 2, booking details and payment
elif st.session_state.page == "booking":
    hotel_data = st.session_state.selected_hotel

    st.button("⬅️ Back to Hotels", on_click=go_to_list)
    st.title(f"Booking: {hotel_data['name']}")

    col_details, col_payment = st.columns([1, 1], gap="large")

    with st.form("booking_master_form"):
        with col_details:
            st.subheader("1. Stay Details")
            full_name = st.text_input("Guest Full Name")

            # date selection (check in , check out)
            today = datetime.now()
            date_range = st.date_input(
                "Select Stay Dates", [today, today + timedelta(days=2)]
            )
            guests = st.number_input(
                "Number of Guests",
                min_value=1,
                max_value=int(hotel_data["capacity"]),
                value=1,
            )
            add_spa = st.checkbox("Include Premium SPA Access")

        with col_payment:
            st.subheader("2. Secure Payment")
            card_num = st.text_input("Card Number (16 digits)")

            c1, c2 = st.columns(2)
            card_exp = c1.text_input("Expiry (MM/YY)")
            card_cvc = c2.text_input("CVC", type="password")

            card_pwd = st.text_input("Security Password", type="password")

            st.info(f"Total to pay: Apply Logic Later")

        # submit button at the bottom
        submit_btn = st.form_submit_button(
            "Complete Reservation", type="primary", use_container_width=True
        )

        if submit_btn:
            card = SecureCreditCard(card_num, card_exp, full_name, card_cvc)

            if not card.validate(df_cards):
                st.error("Payment failed: Invalid card credentials.")
            elif not card.authenticate(card_pwd, dict_security):
                st.error("Payment failed: Incorrect security password.")
            elif len(date_range) < 2:
                st.warning("Please select both Check-in and Check-out dates.")
            else:
                hotel = SpaHotel(
                    hotel_data["id"],
                    hotel_data["name"],
                    hotel_data["city"],
                    hotel_data["capacity"],
                    hotel_data["available"],
                )
                if add_spa:
                    hotel.book_spa()
                hotel.book()

                ticket = ReservationTicket(full_name, hotel)
                st.success("Success! Your room has been reserved.")
                st.balloons()
                st.code(ticket.generate_text(), language="text")
