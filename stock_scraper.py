import requests
from bs4 import BeautifulSoup
import time
import datetime


url = "https://kr.investing.com/indices/us-spx-500-futures?cid=1175153"

output_file = "stock.txt"

def fetch_stock_price():
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        price_div = soup.find('div', {'data-test': 'instrument-price-last'})

        if price_div:
            return price_div.text.strip()
        else:
            return None
    except Exception as e:
        print("Price not found", e)
        return None


def capture_prices():
    print("Starting to capture stock prices every minute...")
    while True:
        start_time = time.time()

        price = fetch_stock_price()
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if price:
            with open(output_file, 'a') as file:
                file.write(f"{current_time}: {price}\n")
            print(f"{current_time}: Captured price: {price}")
        else:
            print(f"{current_time}: Price not found")

        elapsed_time = time.time() - start_time

        time.sleep(10)

if __name__ == "__main__":
    capture_prices()
