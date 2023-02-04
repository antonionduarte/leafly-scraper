#!/bin/bash

if [ "$#" != "1" ]; then
	echo "Error, correct usage: $0 <product_slug>"
	exit 1
fi

product_slug=$1

python3 src/scrape_product.py $product_slug
