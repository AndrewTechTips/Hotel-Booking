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

    # back button and title centered
    _, center_col, _ = st.columns([1, 2, 1])

    with center_col:
        if st.button("⬅️ Back to Hotels"):
            go_to_list()
            st.rerun()

        st.title(f"Book your stay at {hotel_data['name']}")
        st.markdown(f"📍 {hotel_data['city']} | 👥 Max {hotel_data['capacity']} guests")
        st.divider()

        # we wrap everything in a single form for a clean vertical flow

        with st.form("booking_master_form", clear_on_submit=False):
            # 1 stay details
            st.markdown("### 📋 Step 1: Stay Details")
            full_name = st.text_input("Full Name", placeholder="e.g. John Smith")

            col_date, col_guests = st.columns([2, 1])

            with col_date:
                # date selection (check in , check out)
                today = datetime.now()
                date_range = st.date_input(
                    "Check-in & Check-out", [today, today + timedelta(days=2)]
                )
            with col_guests:
                guests = st.number_input(
                    "Guests",
                    min_value=1,
                    max_value=int(hotel_data["capacity"]),
                    value=1,
                )

            add_spa = st.checkbox("Include VIP SPA Package (+ $50)")

            st.markdown("<br>", unsafe_allow_html=True)  # Spacer
            st.divider()

            # 2 secure payment
            st.markdown("### 💳 Step 2: Secure Payment")
            card_num = st.text_input(
                "Card Number", max_chars=16, placeholder="0000 0000 0000 0000"
            )

            c1, c2, c3 = st.columns([2, 1, 1])
            card_exp = c1.text_input("Expiry", placeholder="MM/YY")
            card_cvc = c2.text_input("CVC", type="password", placeholder="***")
            card_pwd = c3.text_input("PIN", type="password", placeholder="****")

            st.markdown("<br>", unsafe_allow_html=True)

            # summary, submit

            st.markdown(
                f"""
                    <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; border-left: 4px solid #3fb950;">
                    <small style="color: #8b949e;">ORDER SUMMARY</small><br>
                    <strong>{hotel_data['name']}</strong> - {guests} Guest(s)<br>
                    <small>Booking guaranteed via SecureCard™</small>
                    </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("<br>", unsafe_allow_html=True)

            submit_btn = st.form_submit_button(
                "Confirm Reservation", type="primary", use_container_width=True
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
