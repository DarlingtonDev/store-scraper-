import json
import requests

'''
Downloads all products from a shopify store and stores as a json file (all_products.json)
'''


def download_json():
    all_products = []
    page = 1
    while True:
        site = f"https://thescentsstore.com/products.json?page={page}"
        req = requests.get(site)
        data = req.json()
        products = data.get("products", [])
        if not products[0]:
            print("error", products)
            break
        for product in products:
            all_products.append(product)
        print(f"page{page} done...proceeding to page{page + 1}")
        page += 1
    with open("all_products.json", "w") as f:
        json.dump(all_products, f, indent=4)
    print("all products saved")


download_json()
