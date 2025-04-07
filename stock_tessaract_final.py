import os
import time
import datetime
import pytesseract
import cv2
import numpy as np
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Path to Tesseract-OCR (Windows users, uncomment & update this path)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Selenium WebDriver setup
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--log-level=3")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = "https://kr.investing.com/indices/us-spx-500-futures?cid=1175153"
driver.get(url)
time.sleep(5)  # Wait for page to load

# Output files
output_file = "all_stock_prices.txt"

# Create folder for screenshots
screenshot_folder = "screenshots"
if not os.path.exists(screenshot_folder):
    os.makedirs(screenshot_folder)

print("Starting stock price monitoring...")

try:
    while True:
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Capture full screenshot
        screenshot_filename = os.path.join(screenshot_folder, f"screenshot_{now}.png")
        driver.save_screenshot(screenshot_filename)
        print(f"Screenshot saved: {screenshot_filename}")

        try:
            # Locate stock price element on the page
            stock_price_element = driver.find_element(By.XPATH,
                                                      "//div[contains(@class, 'text-5xl') or contains(@class, 'instrument-price')]")
            location = stock_price_element.location
            size = stock_price_element.size

            # Open screenshot image
            image = Image.open(screenshot_filename)
            left = location['x']
            top = location['y']
            right = left + size['width']
            bottom = top + size['height']
            cropped_image = image.crop((left, top, right, bottom))

            # Convert cropped image to OpenCV format
            img = cv2.cvtColor(np.array(cropped_image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

            # Apply OCR
            extracted_text = pytesseract.image_to_string(binary, config='--psm 6')

            # Extract valid stock price
            stock_price = "N/A"
            for line in extracted_text.split("\n"):
                line = line.strip()
                if line.replace(",", "").replace(".", "").isdigit():
                    stock_price = line
                    break

        except Exception as e:
            print(f"Error extracting stock price: {e}")
            stock_price = "N/A"

        # Write to text file
        with open(output_file, "a", encoding="utf-8") as file:
            file.write(f"{now}: {stock_price}\n")

        print(f"{now} - Stock Price (OCR): {stock_price}")

        time.sleep(30)

except KeyboardInterrupt:
    print("Stopping stock price monitoring...")

finally:
    driver.quit()
    print("WebDriver closed.")
