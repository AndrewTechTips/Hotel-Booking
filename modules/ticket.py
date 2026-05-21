from abc import ABC, abstractmethod
from datetime import datetime
from fpdf import FPDF


class BaseTicket(ABC):
    """Abstract base class handling document generation layouts."""

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
        pdf.set_margins(20, 20, 20)

        # Solid minimalist top brand header block
        pdf.set_fill_color(9, 10, 15)
        pdf.rect(0, 0, 210, 40, "F")

        pdf.set_text_color(240, 246, 252)
        pdf.set_font("Helvetica", style="B", size=22)
        pdf.ln(5)
        pdf.cell(w=0, h=10, txt="LUXURY BOOKING ENGINE", ln=1, align="L")
        pdf.set_font("Helvetica", style="I", size=10)
        pdf.set_text_color(139, 148, 158)
        pdf.cell(
            w=0, h=5, txt="Official Reservation & Booking Statement", ln=1, align="L"
        )

        pdf.ln(22)
        pdf.set_text_color(30, 30, 30)

        # Statement Overview
        pdf.set_font("Helvetica", style="B", size=11)
        pdf.cell(w=40, h=7, txt="Prepared For:", ln=0)
        pdf.set_font("Helvetica", style="", size=11)
        pdf.cell(w=0, h=7, txt=self._customer_name, ln=1)

        pdf.set_font("Helvetica", style="B", size=11)
        pdf.cell(w=40, h=7, txt="Statement Date:", ln=0)
        pdf.set_font("Helvetica", style="", size=11)
        pdf.cell(w=0, h=7, txt=self._date_generated, ln=1)

        pdf.ln(6)
        pdf.set_draw_color(220, 225, 230)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(8)

        # Property Subheader
        pdf.set_font("Helvetica", style="B", size=15)
        pdf.set_text_color(65, 105, 225)
        pdf.cell(w=0, h=8, txt=self._hotel.name, ln=1)
        pdf.set_font("Helvetica", style="I", size=11)
        pdf.set_text_color(100, 110, 120)
        pdf.cell(w=0, h=6, txt=f"Location context: {self._hotel.city}", ln=1)
        pdf.ln(6)

        # Table Grid Headers
        pdf.set_fill_color(245, 247, 250)
        pdf.set_text_color(50, 50, 50)
        pdf.set_font("Helvetica", style="B", size=10)
        pdf.cell(w=85, h=10, txt=" Itemized Description", border=1, ln=0, fill=True)
        pdf.cell(w=45, h=10, txt=" Arrangement", border=1, ln=0, fill=True)
        pdf.cell(w=40, h=10, txt=" Settle Amount", border=1, ln=1, fill=True, align="R")

        # Structured Rows
        pdf.set_font("Helvetica", style="", size=10)

        pdf.cell(w=85, h=9, txt=" Accommodation Base Stays", border=1, ln=0)
        pdf.cell(
            w=45, h=9, txt=f"{self._check_in} to {self._check_out}", border=1, ln=0
        )
        pdf.cell(
            w=40,
            h=9,
            txt=f"${self._hotel.price_per_night:.2f} / night",
            border=1,
            ln=1,
            align="R",
        )

        spa_status = (
            "Included"
            if (hasattr(self._hotel, "spa_included") and self._hotel.spa_included)
            else "Not Requested"
        )
        spa_fee = (
            50.0
            if (hasattr(self._hotel, "spa_included") and self._hotel.spa_included)
            else 0.0
        )
        pdf.cell(w=85, h=9, txt=" VIP Spa Sanctuary Package Add-on", border=1, ln=0)
        pdf.cell(w=45, h=9, txt=spa_status, border=1, ln=0)
        pdf.cell(w=40, h=9, txt=f"${spa_fee:.2f}", border=1, ln=1, align="R")

        pdf.cell(
            w=85, h=9, txt=" Regional Hospitality Fees & Processing", border=1, ln=0
        )
        pdf.cell(w=45, h=9, txt="Complimentary", border=1, ln=0)
        pdf.cell(w=40, h=9, txt="$0.00", border=1, ln=1, align="R")

        # Summary row
        pdf.ln(6)
        pdf.set_font("Helvetica", style="B", size=13)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(w=130, h=12, txt="Total Net Capital Settled:", ln=0, align="R")
        pdf.set_text_color(63, 185, 80)
        pdf.cell(w=40, h=12, txt=f"${self._total_price:.2f}", ln=1, align="R")

        # Signature Footer Notice
        pdf.ln(35)
        pdf.set_draw_color(240, 240, 240)
        pdf.line(40, pdf.get_y(), 170, pdf.get_y())
        pdf.ln(6)
        pdf.set_font("Helvetica", style="I", size=9)
        pdf.set_text_color(140, 145, 150)
        pdf.cell(
            w=0,
            h=5,
            txt="Thank you for choosing absolute excellence. Enjoy your travels.",
            ln=1,
            align="center",
        )

        pdf.output(filename)
        return filename


class ReservationTicket(BaseTicket):
    def generate_text(self) -> str:
        return f"Reservation confirmed for {self._customer_name}. Total paid: ${self._total_price:.2f}"
