import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta
from modules import SpaHotel, SecureCreditCard, ReservationTicket

# 1. UI Configuration
st.set_page_config(
    page_title="Lux Booking Engine", layout="wide", initial_sidebar_state="collapsed"
)

# Premium CSS
st.markdown(
    """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<style>
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background: linear-gradient(-45deg, #090a0f, #11151f, #0d1218, #161a2b);
        background-size: 400% 400%;
        animation: gradientBG 20s ease infinite;
    }

    /* Cards */
    .hotel-card {
        background: rgba(20, 25, 35, 0.45);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        padding: 25px;
        margin-bottom: 25px;
        height: auto;
        min-height: 320px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .hotel-card:hover {
        transform: translateY(-8px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 15px 45px rgba(65, 105, 225, 0.15);
    }

    /* Checkout Custom Hero Banner */
    .checkout-hero {
        background: rgba(20, 25, 35, 0.4);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 35px 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: inset 0 0 40px rgba(65, 105, 225, 0.05), 0 10px 30px rgba(0,0,0,0.3);
        position: relative;
    }
    .checkout-hero-icon {
        font-size: 2.2em;
        color: #4169e1;
        margin-bottom: 12px;
        text-shadow: 0 0 20px rgba(65, 105, 225, 0.5);
    }

    /* Primary Button Fix (Text Visibility & Premium Hover) */
    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #4169e1, #2b4ba3) !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(65, 105, 225, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stFormSubmitButton"] button p {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.05em !important;
        letter-spacing: 0.5px !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(65, 105, 225, 0.6) !important;
    }

    /* General Typography */
    h1, h2, h3 { color: #f0f6fc; font-family: 'Inter', sans-serif; }
    p { color: #8b949e; font-size: 0.95em; line-height: 1.5; }
    .icon-accent { color: #a1b0c0; width: 20px; text-align: center; margin-right: 8px; }

    .status-available { color: #3fb950; font-weight: 600; font-size: 0.9em; letter-spacing: 0.5px; }
    .status-booked { color: #f85149; font-weight: 600; font-size: 0.9em; letter-spacing: 0.5px; }

    .summary-box {
        background: linear-gradient(135deg, rgba(63, 185, 80, 0.15), rgba(0,0,0,0.2));
        padding: 25px;
        border-radius: 12px;
        margin-top: 25px;
        border: 1px solid rgba(63, 185, 80, 0.3);
        border-left: 5px solid #3fb950;
    }

    .card-title-container {
        display: flex; justify-content: space-between; align-items: flex-start; 
        margin-bottom: 15px; gap: 10px;
    }
    .card-title-container h3 { margin: 0; font-size: 1.35em; line-height: 1.3; }

    .rating-badge {
        background: rgba(255,215,0,0.1); border: 1px solid rgba(255,215,0,0.2);
        color: #ffd700; padding: 4px 12px; border-radius: 20px; 
        font-size: 0.85em; font-weight: bold; white-space: nowrap;
        display: flex; align-items: center; gap: 5px;
    }

    .premium-hero-banner {
        position: relative; height: 220px; border-radius: 16px; margin-bottom: 40px;
        overflow: hidden; background: rgba(15, 20, 30, 0.4);
        border: 1px solid rgba(255,255,255,0.05); display: flex; align-items: center;
        justify-content: center; box-shadow: 0 10px 40px rgba(0,0,0,0.4);
    }
    .premium-hero-banner::before {
        content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
        background: radial-gradient(circle at center, rgba(65, 105, 225, 0.15) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(138, 43, 226, 0.15) 0%, transparent 40%);
        animation: rotateGlow 20s linear infinite; z-index: 1;
    }
    .premium-hero-banner::after {
        content: ''; position: absolute; inset: 0; backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px); z-index: 2;
    }
    .hero-content {
        position: relative; z-index: 3; text-align: center; padding: 0 20px;
    }
    .hero-subtitle {
        color: rgba(255,255,255,0.5); text-transform: uppercase; letter-spacing: 4px;
        font-size: 0.8em; font-weight: 600; display: block; margin-bottom: 8px;
    }

    @keyframes rotateGlow { 100% { transform: rotate(360deg); } }
</style>
""",
    unsafe_allow_html=True,
)


# 2. Data Loading
@st.cache_data
def load_data():
    df_hotels = pd.read_csv("data/hotels.csv", dtype={"id": str})
    df_hotels["price_per_night"] = pd.to_numeric(df_hotels["price_per_night"])
    df_hotels["rating"] = pd.to_numeric(df_hotels["rating"])
    df_hotels["capacity"] = pd.to_numeric(df_hotels["capacity"])

    df_cards = pd.read_csv("data/cards.csv", dtype=str).to_dict(orient="records")
    df_sec = pd.read_csv("data/card-security.csv", dtype=str)
    dict_security = dict(zip(df_sec.number, df_sec.password))
    return df_hotels, df_cards, dict_security


df_hotels, df_cards, dict_security = load_data()

if "page" not in st.session_state:
    st.session_state.page = "list"
if "selected_hotel" not in st.session_state:
    st.session_state.selected_hotel = None


def view_details(hotel_row):
    st.session_state.selected_hotel = hotel_row
    st.session_state.page = "details"


def go_to_booking():
    st.session_state.page = "booking"


def go_to_list():
    st.session_state.selected_hotel = None
    st.session_state.page = "list"


# ==========================================
# PAGE 1: HOTEL EXPLORER
# ==========================================
if st.session_state.page == "list":
    st.markdown(
        "<h1><i class='fa-solid fa-gem' style='color: #4169e1; margin-right: 15px;'></i>Discover Luxury Stays</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-size: 1.1em;'>Find and book exclusive premium destinations around the world.</p><br>",
        unsafe_allow_html=True,
    )

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

# ==========================================
# PAGE 2: HOTEL DETAILS
# ==========================================
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

# ==========================================
# PAGE 3: SECURE CHECKOUT (REDESIGNED & CLEAN)
# ==========================================
elif st.session_state.page == "booking":
    hotel_data = st.session_state.selected_hotel

    _, center_col, _ = st.columns([1, 2.5, 1])

    with center_col:
        st.button(
            "← Back to Details",
            on_click=lambda: setattr(st.session_state, "page", "details"),
        )

        # New Checkout Hero Banner
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

        with st.form("booking_master_form", clear_on_submit=False, border=False):

            st.markdown(
                "<h3 style='font-size: 1.2em; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; margin-bottom: 20px;'><i class='fa-solid fa-clipboard-user icon-accent'></i> Guest Details</h3>",
                unsafe_allow_html=True,
            )

            row1_col1, row1_col2 = st.columns([1, 1])
            with row1_col1:
                full_name = st.text_input(
                    "Primary Guest Name", placeholder="e.g. John Doe"
                )
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

            st.markdown("<br>", unsafe_allow_html=True)
            add_spa = st.checkbox("Include VIP SPA Access (+ $50 flat fee)")

            st.markdown(
                "<br><h3 style='font-size: 1.2em; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; margin-bottom: 20px;'><i class='fa-regular fa-credit-card icon-accent'></i> Payment Method</h3>",
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
            card_pwd = c3.text_input(
                "PIN", type="password", max_chars=4, placeholder="****"
            )

            base_price_per_night = float(hotel_data.get("price_per_night", 120))
            nights = (
                (date_range[1] - date_range[0]).days
                if isinstance(date_range, (list, tuple)) and len(date_range) == 2
                else 0
            )
            total_price = (base_price_per_night * guests * nights) + (
                50 if add_spa else 0
            )

            st.markdown(
                f"""
                <div class="summary-box">
                    <small style="color: #a5d6ff; font-weight: bold; letter-spacing: 1px;"><i class="fa-solid fa-receipt" style="margin-right: 8px;"></i>FINAL SUMMARY</small><br>
                    <span style="font-size: 1.1em; color: #e6edf3; display: inline-block; margin-top: 10px;">{nights} Night(s) for {guests} Guest(s)</span><br>
                    <h2 style="margin-top: 10px; margin-bottom: 0; color: #3fb950; font-size: 2.2em;">Total: ${total_price:.2f}</h2>
                </div>
            """,
                unsafe_allow_html=True,
            )

            st.markdown("<br>", unsafe_allow_html=True)
            submit_btn = st.form_submit_button(
                "Confirm Payment & Book", type="primary", use_container_width=True
            )

        if submit_btn:
            card = SecureCreditCard(card_num, card_exp, full_name, card_cvc)

            if not card.validate(df_cards):
                st.error("Authentication failed: Please check your card details.")
            elif not card.authenticate(card_pwd, dict_security):
                st.error("Security alert: Incorrect card PIN.")
            elif (
                not isinstance(date_range, (list, tuple))
                or len(date_range) < 2
                or nights <= 0
            ):
                st.warning("Please select valid check-in and check-out dates.")
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

                df_hotels.loc[df_hotels["id"] == hotel.id, "available"] = "no"
                df_hotels.to_csv("data/hotels.csv", index=False)
                load_data.clear()

                ticket = ReservationTicket(
                    full_name,
                    hotel,
                    str(date_range[0]),
                    str(date_range[1]),
                    total_price,
                )
                pdf_filename = ticket.generate_pdf(f"ticket_{hotel.id}.pdf")

                st.toast("Payment successful! Generating ticket...", icon="✅")
                st.success(
                    "Your reservation is confirmed. Your digital ticket is ready."
                )
                st.balloons()

                with open(pdf_filename, "rb") as pdf_file:
                    st.download_button(
                        label="Download PDF Ticket",
                        data=pdf_file,
                        file_name=pdf_filename,
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True,
                    )
