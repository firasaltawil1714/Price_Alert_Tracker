import csv
from pathlib import Path
from datetime import date
import requests
from bs4 import BeautifulSoup


class PriceAlertTracker:
    def __init__(self, watch_list, log_path):
        self.watch_list = watch_list
        self.log_path = log_path
        self.deals = []

    def get_product_info(self, url):
        response = requests.get(url)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("h1").text.strip()
        price_text = soup.find("p", class_="price_color").text.strip()
        price = float(price_text.replace("£", "").strip())
        return {"title": title, "price": price}

    def check(self):
        deals = []
        for item in self.watch_list:
            product_info = self.get_product_info(item["url"])
            if product_info["price"] <= item["target_price"]:
                deals.append(product_info)
        self.deals = deals

    def log_deals(self):
        file_exists = self.log_path.exists()
        with open(self.log_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["date", "title", "price"])
            for deal in self.deals:
                writer.writerow([date.today().isoformat(), deal["title"], deal["price"]])

    def run(self):
        print("Checking prices...")
        self.check()
        if self.deals:
            print(f"Found {len(self.deals)} deal(s)!")
            self.log_deals()
            for deal in self.deals:
                print(f" - {deal['title']}: £{deal['price']:.2f}")
        else:
            print("No deals found today.")


if __name__ == "__main__":
    script_dir = Path(__file__).parent
    watch_list = [
        {"url": "https://books.toscrape.com/catalogue/soumission_998/index.html", "target_price": 55.00},
        {"url": "https://books.toscrape.com/catalogue/sharp-objects_997/index.html", "target_price": 40.00},
    ]
    tracker = PriceAlertTracker(watch_list, script_dir / "price_alerts.csv")
    tracker.run()