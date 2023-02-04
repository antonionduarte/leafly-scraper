#!/bin/bash

if [ "$#" != "1" ]; then
	echo "Error, correct usage: $0 <brand_slug>"
	exit 1
fi

brand_slug=$1

python3 src/scrape_brand.py $brand_slug
