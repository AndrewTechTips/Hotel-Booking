<div align="center">

  <h1>🏨 Luxury Booking Engine</h1>

  <p>
    A full-featured <strong>hotel booking application</strong> built with Python and Streamlit.<br />
    Browse hotels, validate payment cards, add spa upgrades, and receive a 
    <strong>generated PDF reservation ticket</strong> — all in one polished dark UI.
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
    <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="pandas" />
    <img src="https://img.shields.io/badge/fpdf2-PDF%20Generation-brightgreen?style=for-the-badge" alt="fpdf2" />
    <img src="https://img.shields.io/badge/OOP-Classes%20%26%20Inheritance-orange?style=for-the-badge" alt="OOP" />
  </p>

  <h3>
    <a href="https://lux-booking.streamlit.app/">🏨 OPEN APP</a>
  </h3>

</div>

<br />

---

## ✨ Features

* **🏩 Hotel Cards:** Each hotel displays name, city, rating, price per night, amenities, and availability status in a glassmorphism card.
* **💳 Card Validation:** Credit card details (number, expiry, holder, CVC) are validated against a CSV dataset before any booking is confirmed.
* **🔐 2-Step Authentication:** `SecureCreditCard` adds a password check on top of standard validation — no booking without both passing.
* **🧖 Spa Upgrade:** Eligible hotels offer an optional VIP Spa add-on, handled via the `SpaHotel` subclass.
* **📄 PDF Ticket Generation:** A formatted A4 reservation statement is generated with `fpdf2` and offered as a download after booking.
* **🎨 Premium Dark UI:** Animated gradient background, glassmorphism cards, hover effects — all injected via `styles.py`.

---

## 🧠 Architecture

The app is split into focused classes, keeping business logic separate from the UI layer.

### `Hotel` & `SpaHotel` — Inheritance
`SpaHotel` extends `Hotel` with spa booking functionality — demonstrating OOP inheritance cleanly:

```python
class SpaHotel(Hotel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spa_included = False

    def book_spa(self):
        self.spa_included = True
```

### `CreditCard` & `SecureCreditCard` — Two-Layer Validation
Standard card data is validated against `cards.csv`. The secure subclass adds a password layer checked against `card-security.csv`:

```python
class SecureCreditCard(CreditCard):
    def authenticate(self, given_password, df_security_dict):
        if self.number in df_security_dict:
            return df_security_dict[self.number] == given_password
        return False
```

### `BaseTicket` & `ReservationTicket` — Abstract Base Class
`BaseTicket` is an ABC that handles all PDF layout logic. `ReservationTicket` only needs to implement `generate_text()` — keeping the PDF generation reusable:

```python
class BaseTicket(ABC):
    @abstractmethod
    def generate_text(self) -> str:
        pass

    def generate_pdf(self, filename="ticket.pdf"):
        # Full A4 PDF layout with header, table, totals, footer...
```

---

## 📁 Project Structure

```
Hotel-Booking/
├── data/
│   ├── hotels.csv          # Hotel data — name, city, price, rating, amenities
│   ├── cards.csv           # Valid card data for payment validation
│   └── card-security.csv   # Card passwords for 2-step authentication
├── modules/
│   ├── __init__.py
│   ├── hotel.py            # Hotel & SpaHotel classes
│   ├── payment.py          # CreditCard & SecureCreditCard classes
│   └── ticket.py           # BaseTicket (ABC) & ReservationTicket
├── utils/
│   ├── __init__.py
│   └── styles.py           # Injected CSS — dark theme & glassmorphism
├── main.py                 # Streamlit UI & booking flow
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

1. **Clone the repository:**
    ```bash
    git clone https://github.com/AndrewTechTips/Luxury-Booking-Engine.git
    cd Luxury-Booking-Engine
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the app:**
    ```bash
    streamlit run main.py
    ```

---

## 📬 Contact

* **LinkedIn:** [Andrei Condrea](https://www.linkedin.com/in/andrei-condrea-b32148346)
* **Email:** condrea.andrey777@gmail.com

<p align="center">
  <i>"Thank you for choosing absolute excellence. Enjoy your travels." 🌍</i>
</p>