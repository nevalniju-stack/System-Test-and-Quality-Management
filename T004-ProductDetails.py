
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.maximize_window()

PRODUCT_URL = (
    "https://opencart.abstracta.us/"
    "index.php?product_id=30&route=product/product"
)

try:
    # SCENARIO 1 - Check main product information

    driver.get(PRODUCT_URL)
    time.sleep(3)

    page_text = driver.find_element(By.TAG_NAME, "body").text

    if "Canon EOS 5D" in page_text and "Canon" in page_text:
        print("Scenario 1: PASS - Product name and brand appeared")
    else:
        print("Scenario 1: FAIL - Product name or brand was missing")

    if "$98.00" in page_text:
        print("Scenario 1: PASS - Expected current price appeared")
    else:
        print("Scenario 1: CHECK - Current price may be different")

    # SCENARIO 2 - Check product description

    driver.get(PRODUCT_URL)
    time.sleep(3)

    page_text = driver.find_element(By.TAG_NAME, "body").text

    description = driver.find_elements(By.ID, "tab-description")

    if description and description[0].text.strip():
        print("Scenario 2: PASS - Product description was displayed")
    elif "Description" in page_text:
        print("Scenario 2: CHECK - Description tab exists; inspect its content")
    else:
        print("Scenario 2: FAIL - Product description was not found")

    if "Reward Points" in page_text:
        print("Scenario 2: PASS - Reward points information appeared")
    else:
        print("Scenario 2: CHECK - Reward points were not found")

    # SCENARIO 3 - Check quantity and purchase controls

    driver.get(PRODUCT_URL)
    time.sleep(3)

    quantity_fields = driver.find_elements(By.NAME, "quantity")

    if quantity_fields:
        quantity = quantity_fields[0]
        quantity.clear()
        quantity.send_keys("1")

        if quantity.get_attribute("value") == "1":
            print("Scenario 3: PASS - Quantity 1 was accepted")
        else:
            print("Scenario 3: FAIL - Quantity 1 was not accepted")

        quantity.clear()
        quantity.send_keys("2")

        if quantity.get_attribute("value") == "2":
            print("Scenario 3: PASS - Quantity 2 was accepted")
        else:
            print("Scenario 3: FAIL - Quantity 2 was not accepted")
    else:
        print("Scenario 3: FAIL - Quantity field was not found")

    add_to_cart = driver.find_elements(By.ID, "button-cart")

    if add_to_cart:
        print("Scenario 3: PASS - Add to Cart control was displayed")
    else:
        print("Scenario 3: FAIL - Add to Cart control was not found")

finally:
    time.sleep(2)
    driver.quit()
