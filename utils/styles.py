import streamlit as st


def inject_premium_styles():
    """Injects premium global styles and typography into the application."""
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
            }
            .checkout-hero-icon {
                font-size: 2.2em;
                color: #4169e1;
                margin-bottom: 12px;
                text-shadow: 0 0 20px rgba(65, 105, 225, 0.5);
            }
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
            .hero-content { position: relative; z-index: 3; text-align: center; padding: 0 20px; }
            .hero-subtitle {
                color: rgba(255,255,255,0.5); text-transform: uppercase; letter-spacing: 4px;
                font-size: 0.8em; font-weight: 600; display: block; margin-bottom: 8px;
            }
            @keyframes rotateGlow { 100% { transform: rotate(360deg); } }
        </style>
        """,
        unsafe_allow_html=True,
    )
