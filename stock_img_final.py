import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# removing SSL errors
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--log-level=3")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = "https://kr.investing.com/indices/us-spx-500-futures?cid=1175153"
driver.get(url)

time.sleep(5)

# make .txt for stock prices
output_file = "all_stock_prices.txt"

# making folder for saving screenshots
screenshot_folder = "screenshots"
if not os.path.exists(screenshot_folder):
    os.makedirs(screenshot_folder)

print("Starting stock price monitoring...")

try:
    while True:
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # capture screenshot
        screenshot_filename = os.path.join(screenshot_folder, f"screenshot_{now}.png")
        driver.save_screenshot(screenshot_filename)
        print(f"Screenshot saved: {screenshot_filename}")

        # find stock price text in the screenshot
        try:
            stock_price_element = driver.find_element(By.XPATH,
                                                      "//div[contains(@class, 'text-5xl') or contains(@class, 'instrument-price')]")
            stock_price = stock_price_element.text.strip()
        except Exception as e:
            print(f"Error finding stock price: {e}")
            stock_price = "N/A"

        # write stripped stock price to .txt file
        with open(output_file, "a", encoding="utf-8") as file:
            file.write(f"{now}: {stock_price}\n")

        # show stock price in the terminal
        print(f"{now} - Stock Price: {stock_price}")

        # screen capturing for every minute
        time.sleep(60)

except KeyboardInterrupt:
    print("Stopping stock price monitoring...")

finally:
    driver.quit()
    print("WebDriver closed.")
