import json

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
