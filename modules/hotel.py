class Hotel:
    def __init__(self, hotel_id, name, city, capacity, available):
        self.id = str(hotel_id)
        self.name = name
        self.city = city
        self.capacity = int(capacity)
        self.available = available.lower() == "yes"

    def book(self):
        if self.available:
            self.available = False
            return True
        return False


class SpaHotel(Hotel):
    def __init__(self, hotel_id, name, city, capacity, available):
        super().__init__(hotel_id, name, city, capacity, available)
        self.spa_included = False

    def book_spa(self):
        self.spa_included = True
