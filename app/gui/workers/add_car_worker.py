from PySide6.QtCore import QRunnable, QObject, Signal, Slot
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
import re


class AddCarSignals(QObject):
    success = Signal(dict)   # emits the car dict on success
    error = Signal(str)      # emits error message on failure


class AddCarWorker(QRunnable):
    """
    Background worker that scrapes a single AutoDeal listing URL,
    builds a car dict, downloads the image, and emits the result.
    """

    def __init__(self, url):
        super().__init__()
        self.url = url.strip()
        self.signals = AddCarSignals()
        self.setAutoDelete(True)

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Referer": "https://www.google.com/"
        })

    @Slot()
    def run(self):
        try:
            # Validate URL
            if "autodeal.com.ph" not in self.url:
                self.signals.error.emit("URL must be from autodeal.com.ph")
                return

            response = self.session.get(self.url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Determine condition from URL
            condition = "Used" if "/used-cars/" in self.url else "New"

            # Title
            title = ""
            title_tag = soup.select_one("header h1") or soup.select_one("h1")
            if title_tag:
                title = title_tag.get_text(strip=True)
            if not title:
                self.signals.error.emit("Could not find car title on the page.")
                return

            # Price
            price = None
            price_tag = soup.select_one("span.price") or soup.select_one("div.price")
            if price_tag:
                raw = price_tag.get_text(strip=True)
                normalized = raw.replace("₱", "").replace("P", "").replace(",", "").strip()
                try:
                    price = float(normalized)
                except ValueError:
                    price = None

            # Image
            image_url = ""
            img_tag = soup.select_one("div.gallery img") or soup.select_one("img.main-image") or soup.select_one("article img")
            if img_tag:
                image_url = img_tag.get("data-src") or img_tag.get("src") or ""

            # Download image locally
            local_image_path = ""
            if image_url:
                try:
                    os.makedirs("data/images", exist_ok=True)
                    filename = os.path.basename(urlparse(image_url).path)
                    filepath = os.path.join("data/images", filename)
                    if not os.path.exists(filepath):
                        img_response = self.session.get(image_url, timeout=10)
                        img_response.raise_for_status()
                        with open(filepath, "wb") as f:
                            f.write(img_response.content)
                    local_image_path = filepath
                except Exception:
                    local_image_path = ""

            # Specs from table
            transmission = ""
            fuel_type = ""
            year = ""
            specs_rows = soup.select("#specs-table-tab tr")
            for row in specs_rows:
                cols = row.find_all("td")
                if len(cols) != 2:
                    continue
                label = cols[0].get_text(strip=True)
                value = cols[1].get_text(strip=True)
                if "Transmission" in label:
                    transmission = value
                elif "Fuel Type" in label or "Energy Source" in label:
                    fuel_type = value

            # Year from title
            match = re.search(r"\b(20\d{2})\b", title)
            if match:
                year = match.group(1)

            # Brand from title using brands.json
            brand = ""
            try:
                import json
                with open("data/raw/brands.json", "r") as f:
                    brands = json.load(f)
                for b in brands:
                    if b.lower() in title.lower():
                        brand = b
                        break
            except Exception:
                pass

            # Model
            model = title
            if brand:
                model = re.sub(re.escape(brand), "", model, flags=re.IGNORECASE).strip()
            model = re.sub(r"\b(19|20)\d{2}\b", "", model).strip()
            model = re.sub(r"\s+", " ", model)

            car = {
                "title": title,
                "price": price,
                "link": self.url,
                "image_url": image_url,
                "local_image_path": local_image_path,
                "brand": brand,
                "model": model,
                "year": year,
                "transmission": transmission,
                "mileage": "Not applicable" if condition == "New" else "",
                "condition": condition,
                "fuel_type": fuel_type,
                "location": "",
            }

            self.signals.success.emit(car)

        except requests.exceptions.Timeout:
            self.signals.error.emit("Request timed out. Check your connection.")
        except requests.exceptions.RequestException as e:
            self.signals.error.emit(f"Network error: {str(e)}")
        except Exception as e:
            self.signals.error.emit(f"Unexpected error: {str(e)}")
