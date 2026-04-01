import json
import os
import requests
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO


driver = webdriver.Edge()
with open("filtered.json", "r") as f:
    matched_list = json.load(f)
folder_path = "images"
os.makedirs(folder_path, exist_ok= True)
found_count = 0
not_found_count = 0
found_list_with_price = []
for matched_item in matched_list:

    count = 1
    found = False
    while count < 6 and not found:
        driver.get(f"https://fragrances.com.ng/niche-perfumes.html?p={count}")
        products_current_page = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-items .product-item")))
        for product in products_current_page:
            try:
                product_img = product.find_element(By.CSS_SELECTOR, ".product-image-container img").get_attribute("src")
                product_name = product.find_element(By.CSS_SELECTOR, ".product-item-name a").text
                product_price = float(product.find_element(By.CSS_SELECTOR, ".price-wrapper .price").text.split(" ")[1:][0].replace(",", ""))
            except StaleElementReferenceException:
                products_current_page = driver.find_elements(By.CSS_SELECTOR, ".product-items .product-item")
                product = next((p for p in products_current_page if p == product), None)
                if not product:
                    continue
                product_img = product.find_element(By.CSS_SELECTOR, ".product-image-container img").get_attribute("src")
                product_name = product.find_element(By.CSS_SELECTOR, ".product-item-name a").text
                product_price = float(
                    product.find_element(By.CSS_SELECTOR, ".price-wrapper .price").text.split(" ")[1:][0].replace(",",
                                                                                                                  ""))
            if matched_item == product_name:
                found = True
                found_list_with_price.append(f"{product_name} - {product_price - 20000}")
                response = requests.get(product_img)
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))
                    image_resized = img.resize((500, 500))
                    file_name = product_name.replace(" ", "-") + ".jpg"
                    save_path = os.path.join(folder_path, file_name)
                    image_resized.save(save_path)
                    print(f"{file_name} saved ✅")
                    found_count += 1
                    break
                else:
                    print(f"error saving image {product_name} - {response.status_code} ❌")
                    break
        if not found:
            count += 1
    if found:
        print(f"found {matched_item} on page {count}")

    else:
        print(f"{matched_item} not found on all 6 pages")
        not_found_count += 1

print(f"found {found_count} items😁, could not find {not_found_count} items")
with open("send_to_gpt.json", "w") as f:
    json.dump(found_list_with_price, f, indent=4)