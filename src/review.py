from dataclasses import dataclass

@dataclass
class Review:
    date: str
    text: str
    rating: int

    def to_dict(self):
        review = {
            "date": self.date,
            "text": self.text,
            "rating": self.rating
        }
        return review


@dataclass
class Product:
    reviews: list[Review]
    product_slug: str


@dataclass
class Brand:
    products: list[Product]
    brand_slug: str
