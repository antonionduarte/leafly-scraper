import requests
import json
import os


from dataclasses import dataclass


LEAFLY_REVIEW_API_URL = "https://consumer-api.leafly.com/api/product_reviews/v1/{product_name}?take={take_amount}&skip={skip}"
LEAFLY_REVIEW_API_DATE = "created"
LEAFLY_REVIEW_API_RATING = "rating"
LEAFLY_REVIEW_API_TEXT = "text"
LEAFLY_REVIEW_API_PRODUCT_SLUG = "slug"


LEAFLY_BRAND_API_URL = "https://consumer-api.leafly.ca/api/brands/v1/{brand_name}/product_catalog?lat=38.731&lon=-9.1373&take={take_amount}&skip={skip}"
LEAFLY_BRAND_API_PRODUCT_SLUG = "slug"


LEAFLY_API_DATA = "data"
LEAFLY_API_METADATA = "metadata"
LEAFLY_API_TOTALCOUNT = "totalCount"
LEAFLY_API_MAX_REQ = 60


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


def request_product_review_amount(product_slug: str) -> int:
    """ Performs API request to obtain the amount of reviews for a product with the given product slug. """

    response = requests.get(
        LEAFLY_REVIEW_API_URL.format(product_name=product_slug, take_amount=0, skip=0)
    )

    json_response = json.loads(response.text)
    amount = json_response[LEAFLY_API_METADATA][LEAFLY_API_TOTALCOUNT]

    return amount


def request_product_reviews(product_slug: str) -> Product:
    """ 
    Performs API request to obtain all the reviews of a product.
    The requests are made in batches of 60 reviews, given that it is the current review limit for each API request.
    """

    amount_left = request_product_review_amount(product_slug)
    already_requested = 0
    reviews = []

    while amount_left > 0:
        to_request = min(amount_left, LEAFLY_API_MAX_REQ)

        response = requests.get(
            LEAFLY_REVIEW_API_URL.format(product_name=product_slug, take_amount=to_request, skip=already_requested)
        )

        already_requested += to_request
        amount_left -= to_request
        json_response = json.loads(response.text)

        for review in json_response[LEAFLY_API_DATA]:
            date = review[LEAFLY_REVIEW_API_DATE]
            rating = int(review[LEAFLY_REVIEW_API_RATING])
            text = review[LEAFLY_REVIEW_API_TEXT]
            reviews.append(Review(date=date, text=text, rating=rating))

    return Product(reviews=reviews, product_slug=product_slug)


def request_brand_products_amount(brand_slug: str) -> int:
    """ Performs API request to obtain the amount of products that the brand with the given brand slug has. """

    response = requests.get(
        LEAFLY_BRAND_API_URL.format(brand_name=brand_slug, take_amount=0, skip=0)
    )

    json_response = json.loads(response.text)
    amount = json_response[LEAFLY_API_METADATA][LEAFLY_API_TOTALCOUNT]

    return amount


def request_brand_products_slugs(brand_slug: str) -> list[str]:
    """ Performs API request to obtain the list of slugs for every product of a brand. """

    amount_left = request_brand_products_amount(brand_slug)
    already_requested = 0
    product_slugs = []

    while amount_left > 0:
        to_request = min(amount_left, LEAFLY_API_MAX_REQ)

        response = requests.get(
            LEAFLY_BRAND_API_URL.format(brand_name=brand_slug, take_amount=to_request, skip=already_requested)
        )

        already_requested += to_request
        amount_left -= to_request
        json_response = json.loads(response.text)

        for product in json_response[LEAFLY_API_DATA]:
            product_slugs.append(product[LEAFLY_BRAND_API_PRODUCT_SLUG])

    return product_slugs


def request_brand_reviews(brand_slug: str) -> Brand:
    """ Performs API request to obtain all the reviews, for each product of the brand with the given brand slug. """

    product_slugs = request_brand_products_slugs(brand_slug)
    products = []

    for product in product_slugs:
        products.append(request_product_reviews(product))

    return Brand(products=products, brand_slug=brand_slug)


def write_product_file(product: Product, path: str):
    """ Writes to a file on the given path, the review information of the given Product in JSON format. """

    if not os.path.exists(path):
        os.makedirs(path)

    reviews_dict = {
        "reviews": []
    }

    for review in product.reviews:
        reviews_dict['reviews'].append(review.to_dict())
    
    filename = f'{product.product_slug}.json'
    file = open(path + filename, "w")
    file.write(json.dumps(reviews_dict))


def write_brand_file(brand: Brand, path: str):
    """ Writes to a file on the given path, the review information of each Product of the Brand, in JSON format. """

    if not os.path.exists(path):
        os.makedirs(path)

    for product in brand.products:
        write_product_file(product, path + brand.brand_slug + "/")
    

if __name__ == "__main__":
    """ This is merely for test purposes, this script is not meant to be called directly """
    # slug = "cbd-delight-llc-artisan-cbd-oil-with-blue-dream-terpenes"
    # slug = "medplex-delta-8-thc-chocolate-bites-vegan-kush-mints-indica-delta-8-thc-edibles"
    # product = request_product_reviews(slug)
    # write_product_file(product, OUTPUT_DIRECTORY_REVIEWS)

    # brand_slug = "medplex"
    # brand = request_brand_reviews(brand_slug)
    # write_brand_file(brand, OUTPUT_DIRECTORY_BRANDS)
    pass
