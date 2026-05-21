import streamlit as st

# Application Configuration
st.set_page_config(
    page_title="Lux Booking Engine", layout="wide", initial_sidebar_state="collapsed"
)

import pandas as pd
import time
import os

from datetime import datetime, timedelta
from modules import SpaHotel, SecureCreditCard, ReservationTicket
from utils.styles import inject_premium_styles

# Initialize our custom CSS styles
inject_premium_styles()


@st.cache_data
def load_data():
    """Loads and formats the application data safely across environments."""
    # Build absolute paths to avoid cloud deployment directory issues
    base_dir = os.path.dirname(os.path.abspath(__file__))
    hotels_path = os.path.join(base_dir, "data", "hotels.csv")
    cards_path = os.path.join(base_dir, "data", "cards.csv")
    security_path = os.path.join(base_dir, "data", "card-security.csv")

    # Load and cast hotel metrics for accurate sorting and filtering
    df_hotels = pd.read_csv(hotels_path, dtype={"id": str})
    df_hotels["price_per_night"] = pd.to_numeric(df_hotels["price_per_night"])
    df_hotels["rating"] = pd.to_numeric(df_hotels["rating"])
    df_hotels["capacity"] = pd.to_numeric(df_hotels["capacity"])

    # Format payment records for fast lookups
    df_cards = pd.read_csv(cards_path, dtype=str).to_dict(orient="records")
    df_sec = pd.read_csv(security_path, dtype=str)
    dict_security = dict(zip(df_sec.number, df_sec.password))

    return df_hotels, df_cards, dict_security


df_hotels, df_cards, dict_security = load_data()

# Manage the user's current view within the app
if "page" not in st.session_state:
    st.session_state.page = "list"
if "selected_hotel" not in st.session_state:
    st.session_state.selected_hotel = None


# Navigation helpers
def view_details(hotel_row):
    st.session_state.selected_hotel = hotel_row
    st.session_state.page = "details"


def go_to_booking():
    st.session_state.page = "booking"


def go_to_list():
    st.session_state.selected_hotel = None
    st.session_state.page = "list"


# Page 1, hotel catalog & search

if st.session_state.page == "list":
    st.markdown(
        "<h1><i class='fa-solid fa-gem' style='color: #4169e1; margin-right: 15px;'></i>Discover Luxury Stays</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-size: 1.1em;'>Find and book exclusive premium destinations around the world.</p><br>",
        unsafe_allow_html=True,
    )

    # Search and filter controls
    f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns(
        [2.5, 1.5, 1, 1, 1], gap="medium"
    )
    with f_col1:
        search_query = st.text_input(
            "Search Location", placeholder="City or Hotel Name..."
        )
    with f_col2:
        sort_by = st.selectbox(
            "Sort Results",
            [
                "Recommended",
                "Price: Low to High",
                "Price: High to Low",
                "Highest Rated",
            ],
        )
    with f_col3:
        min_guests = st.number_input("Min Guests", min_value=1, max_value=10, value=1)
    with f_col4:
        min_rating = st.selectbox("Min Rating", ["Any", "4.0+", "4.5+", "4.8+"])
    with f_col5:
        st.markdown("<div style='margin-top: 32px;'>", unsafe_allow_html=True)
        only_avail = st.checkbox("Available Only")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        "<hr style='border: 1px solid rgba(255,255,255,0.05); margin-bottom: 30px;'>",
        unsafe_allow_html=True,
    )

    # Apply user filters to the data
    df_display = df_hotels.copy()

    if search_query:
        query_lower = search_query.lower()
        df_display = df_display[
            df_display.apply(
                lambda row: query_lower in str(row["name"]).lower()
                or query_lower in str(row["city"]).lower(),
                axis=1,
            )
        ]

    df_display = df_display[df_display["capacity"] >= min_guests]

    if min_rating != "Any":
        rating_threshold = float(min_rating.replace("+", ""))
        df_display = df_display[df_display["rating"] >= rating_threshold]

    if only_avail:
        df_display = df_display[df_display["available"] == "yes"]

    if sort_by == "Price: Low to High":
        df_display = df_display.sort_values(by="price_per_night", ascending=True)
    elif sort_by == "Price: High to Low":
        df_display = df_display.sort_values(by="price_per_night", ascending=False)
    elif sort_by == "Highest Rated":
        df_display = df_display.sort_values(by="rating", ascending=False)

    # Render the results
    if df_display.empty:
        st.markdown(
            """
            <div style="text-align: center; padding: 50px 20px; background: rgba(255,255,255,0.02); border-radius: 16px; border: 1px dashed rgba(255,255,255,0.1);">
                <i class="fa-solid fa-magnifying-glass" style="font-size: 3em; color: #8b949e; margin-bottom: 20px;"></i>
                <h3 style="color: #a1b0c0;">No destinations found</h3>
                <p>Try adjusting your search criteria or removing some filters.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        cols = st.columns(3, gap="large")
        df_display = df_display.reset_index(drop=True)

        for index, row in df_display.iterrows():
            with cols[index % 3]:
                is_available = row["available"] == "yes"
                status_class = "status-available" if is_available else "status-booked"
                status_text = "● AVAILABLE NOW" if is_available else "● FULLY BOOKED"

                st.markdown(
                    f"""
                <div class="hotel-card">
                    <div>
                        <div class="card-title-container">
                            <h3>{row['name']}</h3>
                            <span class="rating-badge"><i class="fa-solid fa-star"></i> {row['rating']}</span>
                        </div>
                        <p style="margin-bottom: 8px;"><i class="fa-solid fa-location-dot icon-accent"></i> {row['city']}</p>
                        <p style="margin-bottom: 8px;"><i class="fa-solid fa-user-group icon-accent"></i> Up to {row['capacity']} guests</p>
                        <p style="margin-bottom: 8px; color: #a1b0c0; font-size: 0.85em;"><i class="fa-solid fa-bed icon-accent"></i> {row.get('bed_type', 'Standard Layout')}</p>
                        <p style="color: #e6edf3; font-weight: bold; margin-top: 20px; font-size: 1.15em;">${row['price_per_night']} <span style="font-size: 0.8em; font-weight: normal; color: #8b949e;">/ night</span></p>
                        <div style="margin-top: 15px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 15px;">
                            <span class="{status_class}">{status_text}</span>
                        </div>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
                st.button(
                    "View Property",
                    key=f"view_{row['id']}",
                    on_click=view_details,
                    args=(row.to_dict(),),
                    use_container_width=True,
                )

# Page 2, property details

elif st.session_state.page == "details":
    h = st.session_state.selected_hotel
    is_avail = h["available"] == "yes"

    st.button("← Back to Destinations", on_click=go_to_list)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; margin-bottom: 15px;">
        <h1 style="margin: 0; font-size: clamp(1.8em, 4vw, 2.5em); font-weight: 700;">{h['name']}</h1>
        <div style="background: rgba(255, 215, 0, 0.05); border: 1px solid rgba(255, 215, 0, 0.2); padding: 8px 16px; border-radius: 20px; display: flex; align-items: center; gap: 8px;">
            <i class="fa-solid fa-star" style="color: #ffd700; font-size: 1.1em;"></i>
            <span style="color: #ffd700; font-weight: 800; font-size: 1.1em;">{h['rating']}</span>
            <span style="color: #8b949e; font-size: 0.9em;">/ 5.0</span>
        </div>
    </div>
    <div style="display: flex; gap: 25px; color: #8b949e; font-size: 1.05em; margin-bottom: 25px; flex-wrap: wrap;">
        <span><i class="fa-solid fa-location-dot" style="margin-right: 5px;"></i> {h['city']}</span>
        <span><i class="fa-solid fa-eye" style="margin-right: 5px;"></i> {h.get('view_type', 'Standard View')}</span>
        <span><i class="fa-solid fa-tag" style="margin-right: 5px;"></i> <strong style="color: #e6edf3;">${h['price_per_night']}</strong> / night</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
    <div class="premium-hero-banner">
        <div class="hero-content">
            <span class="hero-subtitle">Exclusive Property Showcase</span>
            <h2 style="margin: 0; font-size: 2em; font-weight: 300; letter-spacing: 1px;">Experience {h['city']} like never before.</h2>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col_info, col_spacer, col_action = st.columns([1.8, 0.1, 1])

    with col_info:
        tab1, tab2, tab3 = st.tabs(["The Story", "Amenities", "Policies"])

        with tab1:
            st.markdown(
                f"<div style='line-height: 1.8; color: #a1b0c0; font-size: 1.1em; padding-top: 15px; text-align: justify;'>{h['description']}</div>",
                unsafe_allow_html=True,
            )

        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            amenities_html = "<div style='display: flex; flex-wrap: wrap; gap: 12px;'>"
            for am in str(h["amenities"]).split("|"):
                amenities_html += f"<span style='background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); padding: 10px 18px; border-radius: 8px; font-size: 0.95em; color: #c9d1d9;'><i class='fa-solid fa-check' style='color: #4169e1; margin-right: 8px;'></i>{am.strip()}</span>"
            amenities_html += "</div>"
            st.markdown(amenities_html, unsafe_allow_html=True)

        with tab3:
            st.markdown(
                f"""
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; background: rgba(255,255,255,0.02); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); margin-top: 15px;">
                <div><i class="fa-regular fa-clock icon-accent"></i> <strong>Check-in:</strong><br> <span style="margin-left: 28px; color: #a1b0c0;">After 15:00</span></div>
                <div><i class="fa-solid fa-person-walking-arrow-right icon-accent"></i> <strong>Check-out:</strong><br> <span style="margin-left: 28px; color: #a1b0c0;">Before 11:00</span></div>
                <div><i class="fa-solid fa-bed icon-accent"></i> <strong>Configuration:</strong><br> <span style="margin-left: 28px; color: #a1b0c0;">{h.get('bed_type', 'Standard')}</span></div>
                <div><i class="fa-solid fa-user-group icon-accent"></i> <strong>Capacity:</strong><br> <span style="margin-left: 28px; color: #a1b0c0;">Up to {h['capacity']} guests</span></div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with col_action:
        st.markdown(
            """
        <div style="background: rgba(20, 25, 35, 0.45); backdrop-filter: blur(16px); padding: 35px 25px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); text-align: center; box-shadow: 0 15px 40px rgba(0,0,0,0.4);">
            <h3 style="margin-top: 0; color: #f0f6fc;"><i class="fa-solid fa-calendar-check" style="margin-right: 10px;"></i>Reserve Stay</h3>
            <p style="color: #8b949e; font-size: 0.95em; margin-bottom: 30px;">Secure your dates in seconds.</p>
        """,
            unsafe_allow_html=True,
        )

        if is_avail:
            st.markdown(
                """
            <div style="display: inline-block; background: rgba(63, 185, 80, 0.15); border: 1px solid rgba(63, 185, 80, 0.4); color: #3fb950; padding: 8px 20px; border-radius: 20px; font-weight: 600; font-size: 0.95em; margin-bottom: 25px;">
                <i class="fa-solid fa-check-circle" style="margin-right: 5px;"></i> Room Available
            </div>
            """,
                unsafe_allow_html=True,
            )
            st.button(
                "Proceed to Checkout",
                on_click=go_to_booking,
                type="primary",
                use_container_width=True,
            )
        else:
            st.markdown(
                """
            <div style="display: inline-block; background: rgba(248, 81, 73, 0.15); border: 1px solid rgba(248, 81, 73, 0.4); color: #f85149; padding: 8px 20px; border-radius: 20px; font-weight: 600; font-size: 0.95em; margin-bottom: 25px;">
                <i class="fa-solid fa-xmark-circle" style="margin-right: 5px;"></i> Fully Booked
            </div>
            """,
                unsafe_allow_html=True,
            )
            st.button("Join Waitlist", disabled=True, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Page 3, secure checkout

elif st.session_state.page == "booking":
    hotel_data = st.session_state.selected_hotel

    # Wide center column for the checkout form
    _, center_col, _ = st.columns([1, 2.5, 1])

    with center_col:
        st.button(
            "← Back to Details",
            on_click=lambda: setattr(st.session_state, "page", "details"),
        )

        st.markdown(
            f"""
            <div class="checkout-hero">
                <div class="checkout-hero-icon"><i class="fa-solid fa-shield-halved"></i></div>
                <h1 style="margin: 0; font-size: 2.2em; font-weight: 300; letter-spacing: 1px;">Secure Reservation</h1>
                <p style="color: #a1b0c0; font-size: 1.1em; margin-top: 10px; margin-bottom: 0;">
                    <i class="fa-solid fa-location-dot" style="margin-right: 5px;"></i> {hotel_data['name']} &mdash; {hotel_data['city']}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # step 1: Stay Configuration (Updating price in real-time without form submission)
        st.markdown(
            "<h3 style='font-size: 1.2em; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; margin-bottom: 20px;'><i class='fa-solid fa-clipboard-user icon-accent'></i> Guest Details</h3>",
            unsafe_allow_html=True,
        )

        row1_col1, row1_col2 = st.columns([1, 1])
        with row1_col1:
            full_name = st.text_input("Primary Guest Name", placeholder="e.g. John Doe")
        with row1_col2:
            guests = st.number_input(
                "Number of Guests",
                min_value=1,
                max_value=int(hotel_data["capacity"]),
                value=1,
            )

        today = datetime.now()
        date_range = st.date_input(
            "Check-in & Check-out Dates", [today, today + timedelta(days=2)]
        )
        add_spa = st.checkbox("Include VIP Spa Sanctuary Access (+ $50 flat fee)")

        # Execute real-time pricing math
        base_price_per_night = float(hotel_data.get("price_per_night", 120))
        nights = (
            (date_range[1] - date_range[0]).days
            if isinstance(date_range, (list, tuple)) and len(date_range) == 2
            else 0
        )
        total_price = (base_price_per_night * guests * nights) + (50 if add_spa else 0)

        st.markdown(
            f"""
            <div class="summary-box">
                <small style="color: #a5d6ff; font-weight: bold; letter-spacing: 1px;"><i class="fa-solid fa-receipt" style="margin-right: 8px;"></i>LIVE CALCULATION SUMMARY</small><br>
                <span style="font-size: 1.1em; color: #e6edf3; display: inline-block; margin-top: 10px;">{nights} Night(s) for {guests} Guest(s)</span><br>
                <h2 style="margin-top: 10px; margin-bottom: 0; color: #3fb950; font-size: 2.2em;">Total Due: ${total_price:.2f}</h2>
            </div>
            <br>
        """,
            unsafe_allow_html=True,
        )

        # step 2: Payment Authorization
        with st.form("payment_form", clear_on_submit=False, border=False):
            st.markdown(
                "<h3 style='font-size: 1.2em; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; margin-bottom: 20px;'><i class='fa-regular fa-credit-card icon-accent'></i> Payment Clearing Method</h3>",
                unsafe_allow_html=True,
            )
            card_num = st.text_input(
                "Card Number", max_chars=16, placeholder="0000 0000 0000 0000"
            )

            c1, c2, c3 = st.columns([2, 1, 1])
            card_exp = c1.text_input("Expiry Date", placeholder="MM/YY")
            card_cvc = c2.text_input(
                "CVC", type="password", max_chars=3, placeholder="***"
            )
            card_pwd = c3.text_input("PIN", type="password", placeholder="****")

            submit_btn = st.form_submit_button(
                "Authorize Secure Transaction", use_container_width=True
            )

        # Handle transaction validation
        if submit_btn:
            card = SecureCreditCard(card_num, card_exp, full_name, card_cvc)

            if not card.validate(df_cards):
                st.error(
                    "Transaction declined: Please verify your credit card parameters."
                )
            elif not card.authenticate(card_pwd, dict_security):
                st.error("Security authorization alert: Invalid card PIN combination.")
            elif (
                not isinstance(date_range, (list, tuple))
                or len(date_range) < 2
                or nights <= 0
            ):
                st.warning(
                    "Please ensure check-in and check-out dates are populated correctly."
                )
            else:
                with st.spinner("Encrypting connection and processing payment..."):
                    time.sleep(1.5)

                hotel = SpaHotel(
                    hotel_data["id"],
                    hotel_data["name"],
                    hotel_data["city"],
                    hotel_data["capacity"],
                    hotel_data["available"],
                    hotel_data["price_per_night"],
                    hotel_data["rating"],
                    hotel_data["amenities"],
                    hotel_data["description"],
                )

                if add_spa:
                    hotel.book_spa()
                hotel.book()

                # Update local database state
                df_hotels.loc[df_hotels["id"] == hotel.id, "available"] = "no"
                df_hotels.to_csv("data/hotels.csv", index=False)
                load_data.clear()

                # Generate the premium PDF receipt
                ticket = ReservationTicket(
                    full_name,
                    hotel,
                    str(date_range[0]),
                    str(date_range[1]),
                    total_price,
                )
                pdf_filename = ticket.generate_pdf(f"ticket_{hotel.id}.pdf")

                st.toast(
                    "Settlement successful. Assembling documentation...", icon="✅"
                )
                st.success(
                    "Your luxury escape has been successfully finalized. Your statement is prepared."
                )
                st.balloons()

                with open(pdf_filename, "rb") as pdf_file:
                    st.download_button(
                        label="Download PDF Invoice Statement",
                        data=pdf_file,
                        file_name=pdf_filename,
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True,
                    )
