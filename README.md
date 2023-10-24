# leafly-scraper

Sorta-scraper (i just saw which HTTP requests were being made to their API and implemented them) for [Leafly](https://www.leafly.com/).

## Current results:

Scraping brand `medplex` with 41 products and around 6650 reviews, in more-a-less 1min20s.

## Data Format

Probably should have classes for:
 - Review 
 - Brand

In which a brand is basically a list of reviews.
A Brand can probably be a collection of reviews 

## Output format 

For single reviews: 
`out/{product_name}`

For brands:
`out/{brand_name}/{product_name}`


## TODO

- [ ] Should probably rework the Data 
