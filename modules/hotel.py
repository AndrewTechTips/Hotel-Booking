class Hotel:
    def __init__(
        self,
        hotel_id,
        name,
        city,
        capacity,
        available,
        price_per_night=0,
        rating=0.0,
        amenities="",
        description="",
    ):
        self.id = str(hotel_id)
        self.name = name
        self.city = city
        self.capacity = int(capacity)
        self.available = str(available).lower() == "yes"

        # New rich data attributes
        self.price_per_night = float(price_per_night)
        self.rating = float(rating)
        self.amenities = amenities.split("|") if amenities else []
        self.description = description

    def book(self):
        if self.available:
            self.available = False
            return True
        return False


class SpaHotel(Hotel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spa_included = False

    def book_spa(self):
        self.spa_included = True
