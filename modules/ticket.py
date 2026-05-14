class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name.title().strip()
        self.hotel = hotel_object

    def generate_text(self):
        content = f"""
        ---Booking Confiramtion---
        Customer number: {self.customer_name}
        Hotel: {self.hotel.name}
        City: {self.hotel.city}
        Spa includes: {'Yes' if hasattr(self.hotel, 'spa_included') and self.hotel.spa_included else 'No'}
        """
        return content

    def generate_pdf(self, filename):
        pass  # Todo
