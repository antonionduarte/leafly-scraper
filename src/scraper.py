import requests
import json
import os


from review import Review


LEAFLY_REVIEW_API_URL = "https://consumer-api.leafly.com/api/product_reviews/v1/{product_name}?take={take_amount}"
LEAFLY_REVIEW_API_DATE = "created"
LEAFLY_REVIEW_API_RATING = "rating"
LEAFLY_REVIEW_API_TEXT = "text"


LEAFLY_BRAND_API_URL = "https://consumer-api.leafly.ca/api/brands/v1/{brand_name}/product_catalog?lat=38.731&lon=-9.1373&take={take_amount}"
LEAFLY_BRAND_API_PRODUCT_SLUG = "slug"


LEAFLY_API_DATA = "data"
LEAFLY_API_METADATA = "metadata"
LEAFLY_API_TOTALCOUNT = "totalCount"


OUTPUT_DIRECTORY = "./out"  


test_uri = "cbd-delight-llc-artisan-cbd-oil-with-blue-dream-terpenes"


def request_product_review_amount(product_slug: str) -> int:
    response = requests.get(
        LEAFLY_REVIEW_API_URL.format(product_name=product_slug, take_amount=0)
    )

    json_response = json.loads(response.text)
    amount = json_response[LEAFLY_API_METADATA][LEAFLY_API_TOTALCOUNT]

    return amount


def request_product_reviews(product_slug: str, amount: int) -> list[Review]:
    response = requests.get(
        LEAFLY_REVIEW_API_URL.format(product_name=product_slug, take_amount=amount)
    )    

    reviews = []
    json_response = json.loads(response.text)

    for review in json_response[LEAFLY_API_DATA]:
        date = review[LEAFLY_REVIEW_API_DATE]
        rating = int(review[LEAFLY_REVIEW_API_RATING])
        text = review[LEAFLY_REVIEW_API_TEXT]
        reviews.append(Review(date=date, text=text, rating=rating))
    
    return reviews


def request_brand_products_amount(brand_slug: str) -> int:
    response = requests.get(
        LEAFLY_BRAND_API_URL.format(brand_name=brand_slug, take_amount=0)
    )

    json_response = json.loads(response.text)
    amount = json_response[LEAFLY_API_METADATA][LEAFLY_API_TOTALCOUNT]

    return amount


def reviews_to_file(reviews: list[Review], product_slug: str):
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    reviews_dict = {
        "reviews": []
    }

    for review in reviews:
        reviews_dict['reviews'].append(review.to_dict())
    
    filename = f'{product_slug}.json'
    file = open(OUTPUT_DIRECTORY + "/" + filename, "w")
    file.write(json.dumps(reviews_dict))


if __name__ == "__main__":
    amount = request_product_review_amount(test_uri)
    reviews = request_product_reviews(test_uri, amount)
    reviews_to_file(reviews, test_uri)
