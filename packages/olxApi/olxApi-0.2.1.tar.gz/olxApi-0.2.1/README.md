

# Description

'olxapi' Is a python module designed to scrape with OLX website. It enable user programmatically search for products and retrieve a sorted list by ID, Title, Price, Thumbnail and Link of the ads."


# instalation

``` pip install olxapi  ```


# Features

-Search for products on OLX.
-Retrieve a list of ads with details like thumbnail, title, price, and permalink.
-Limit the number of pages to scrape.

# How to Use

` from olxapi import OlxApi `
` product = "Macbook pro" `
` page_limit = 2 `
` olx = OlxApi(page_limit) `
` ads = olx.get_list_product(product) `
` print(ads) `


