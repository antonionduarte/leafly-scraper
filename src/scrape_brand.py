import sys
import scraper

OUTPUT_DIRECTORY_BRANDS = "./out/brands/"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Error, correct usage: scrape_brand.py <brand_slug>')
        exit()

    brand_slug = sys.argv[1]
    brand = scraper.request_brand_reviews(brand_slug)
    scraper.write_brand_file(brand, OUTPUT_DIRECTORY_BRANDS)
