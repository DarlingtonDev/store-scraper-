from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
driver = webdriver.Edge()


def get_pagination_count():
    product_dict = {}
    count = 1
    product_array = []
    while count < 6:
        driver.get(f"https://fragrances.com.ng/niche-perfumes.html?p={count}")
        products = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-items .product-item")))
        for product in products:
            name = product.find_element(By.CSS_SELECTOR, ".product-item-link").text.strip()
            product_array.append(name)
        product_dict[count] = product_array
        count += 1
        product_array = []
    print(product_dict)
    with open("products.json", "w") as f:
        json.dump(product_dict, f, indent=4)
    print("saved products")


get_pagination_count()
