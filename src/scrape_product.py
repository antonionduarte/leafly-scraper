import sys
import scraper

OUTPUT_DIRECTORY_PRODUCTS = "./out/products/"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Error, correct usage: scrape_product.py <product_slug>')
        exit()

    product_slug = sys.argv[1]
    product = scraper.request_product_reviews(product_slug)
    scraper.write_product_file(product, OUTPUT_DIRECTORY_PRODUCTS)
