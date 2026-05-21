from abc import ABC, abstractmethod
from datetime import datetime
from fpdf import FPDF


class BaseTicket(ABC):
    def __init__(
        self,
        customer_name: str,
        hotel_object,
        check_in: str,
        check_out: str,
        total_price: float,
    ):
        self._customer_name = customer_name.strip().title()
        self._hotel = hotel_object
        self._check_in = check_in
        self._check_out = check_out
        self._total_price = total_price
        self._date_generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @abstractmethod
    def generate_text(self) -> str:
        pass

    def generate_pdf(self, filename="ticket.pdf"):
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        # header
        pdf.set_font("Helvetica", style="B", size=16)
        pdf.cell(w=0, h=10, txt=f"Guest Name: {self._customer_name}", ln=1)
        pdf.cell(w=0, h=10, txt=f"Hotel: {self._hotel.name} ({self._hotel.city})", ln=1)
        pdf.cell(
            w=0,
            h=10,
            txt=f"Check-in: {self._check_in} | Check-out: {self._check_out}",
            ln=1,
        )

        spa_status = (
            "Included"
            if (hasattr(self._hotel, "spa_included") and self._hotel.spa_included)
            else "Not Included"
        )
        pdf.cell(w=0, h=10, txt=f"VIP SPA Package: {spa_status}", ln=1)

        # footer and price
        pdf.set_font("Helvetica", style="B", size=14)
        pdf.cell(w=0, h=15, txt=f"Total Paid: ${self._total_price:.2f}", ln=1)

        pdf.output(filename)
        return filename


class ReservationTicket(BaseTicket):
    def generate_text(self) -> str:
        return (
            f"✅ CONFIRMATION FOR {self._customer_name.upper()}\n"
            f"Hotel: {self._hotel.name}\n"
            f"Dates: {self._check_in} to {self._check_out}\n"
            f"Total Paid: ${self._total_price:.2f}"
        )
