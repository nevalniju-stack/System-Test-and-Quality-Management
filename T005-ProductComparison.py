
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.maximize_window()

CANON_URL = (
    "https://opencart.abstracta.us/"
    "index.php?product_id=30&route=product/product"
)

NIKON_URL = (
    "https://opencart.abstracta.us/"
    "index.php?product_id=31&route=product/product"
)

COMPARE_URL = (
    "https://opencart.abstracta.us/"
    "index.php?route=product/compare"
)

def add_to_comparison(product_url, product_name):
    driver.get(product_url)
    time.sleep(3)

    # Find the product comparison button.
    buttons = driver.find_elements(By.ID, "button-compare")

    if not buttons:
        buttons = driver.find_elements(
            By.CSS_SELECTOR, "button[onclick*='compare.add']"
        )

    if buttons:
        buttons[0].click()
        time.sleep(2)
        print(product_name + ": Compare button clicked")
    else:
        print(product_name + ": Compare button not found")

try:
    # SCENARIO 1 - Add two products to comparison

    add_to_comparison(CANON_URL, "Canon EOS 5D")
    add_to_comparison(NIKON_URL, "Nikon D300")

    driver.get(COMPARE_URL)
    time.sleep(3)

    page_text = driver.find_element(By.TAG_NAME, "body").text

    if "Canon EOS 5D" in page_text and "Nikon D300" in page_text:
        print("Scenario 1: PASS - Both products appeared in comparison")
    else:
        print("Scenario 1: FAIL - Both products were not found in comparison")

    # SCENARIO 2 - Check compared product details

    if "Canon EOS 5D" in page_text:
        print("Scenario 2: PASS - Canon EOS 5D appeared")
    else:
        print("Scenario 2: FAIL - Canon EOS 5D was missing")

    if "Nikon D300" in page_text:
        print("Scenario 2: PASS - Nikon D300 appeared")
    else:
        print("Scenario 2: FAIL - Nikon D300 was missing")

    if "Price" in page_text or "$" in page_text:
        print("Scenario 2: PASS - Price information appeared")
    else:
        print("Scenario 2: CHECK - Price information was not found")

    # SCENARIO 3 - Remove a product from comparison

    driver.get(COMPARE_URL)
    time.sleep(3)

    # Locate a Remove button or link on the comparison page.
    remove_buttons = driver.find_elements(
        By.XPATH,
        "//*[self::a or self::button or self::input]"
        "[contains(translate(normalize-space(.),"
        "'REMOVE','remove'),'remove') "
        "or contains(@value,'Remove')]"
    )

    if remove_buttons:
        remove_buttons[0].click()
        time.sleep(3)

        page_text = driver.find_element(By.TAG_NAME, "body").text

        if "Nikon D300" in page_text and "Canon EOS 5D" not in page_text:
            print("Scenario 3: PASS - Canon removed; Nikon remained")
        else:
            print("Scenario 3: CHECK - Inspect comparison page after removal")
    else:
        print("Scenario 3: FAIL - Remove control was not found")

finally:
    time.sleep(2)
    driver.quit()
