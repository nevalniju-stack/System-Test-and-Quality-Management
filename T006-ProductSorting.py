
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

CATEGORY_URL = (
    "https://opencart.abstracta.us/"
    "index.php?path=33&route=product/category"
)

try:
    # SCENARIO 1 - Sort prices from lowest to highest

    driver.get(CATEGORY_URL)
    wait.until(EC.presence_of_element_located((By.ID, "input-sort")))

    sort_dropdown = Select(driver.find_element(By.ID, "input-sort"))

    low_option = next(
        (option for option in sort_dropdown.options
         if "Price (Low > High)" in option.text),
        None
    )

    if low_option:
        # Save the text BEFORE selecting because the page may reload.
        selected_text = low_option.text

        sort_dropdown.select_by_visible_text(selected_text)

        wait.until(EC.staleness_of(
            driver.find_element(By.ID, "input-sort")
        )) if False else None

        time.sleep(3)

        print("Scenario 1: PASS - Selected:", selected_text)
    else:
        print("Scenario 1: FAIL - Lowest-to-highest option not found")

    # SCENARIO 2 - Sort prices from highest to lowest

    driver.get(CATEGORY_URL)
    wait.until(EC.presence_of_element_located((By.ID, "input-sort")))

    sort_dropdown = Select(driver.find_element(By.ID, "input-sort"))

    high_option = next(
        (option for option in sort_dropdown.options
         if "Price (High > Low)" in option.text),
        None
    )

    if high_option:
        # Save the text BEFORE selecting because the page may reload.
        selected_text = high_option.text

        sort_dropdown.select_by_visible_text(selected_text)
        time.sleep(3)

        print("Scenario 2: PASS - Selected:", selected_text)
    else:
        print("Scenario 2: FAIL - Highest-to-lowest option not found")

    # SCENARIO 3 - Change the number of products displayed

    driver.get(CATEGORY_URL)
    wait.until(EC.presence_of_element_located((By.ID, "input-limit")))

    limit_dropdown = Select(driver.find_element(By.ID, "input-limit"))

    limit_option = next(
        (option for option in limit_dropdown.options
         if option.get_attribute("value") == "25"),
        None
    )

    if limit_option:
        selected_text = limit_option.text
        limit_dropdown.select_by_visible_text(selected_text)
        time.sleep(3)

        products = driver.find_elements(
            By.CSS_SELECTOR, ".product-layout"
        )

        print("Scenario 3: Selected display limit:", selected_text)
        print("Product cards displayed:", len(products))
    else:
        print("Scenario 3: FAIL - Display limit 25 was not available")

finally:
    time.sleep(2)
    driver.quit()
