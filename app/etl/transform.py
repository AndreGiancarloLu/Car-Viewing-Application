import os
import json
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from pathlib import Path

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "https://www.google.com/"
})

def download_image(url, save_dir="data/images"):
    try:
        os.makedirs(save_dir, exist_ok=True)
        filename = os.path.basename(urlparse(url).path)
        filepath = os.path.join(save_dir, filename)

        if not os.path.exists(filepath):
            response = session.get(url, timeout=10)
            response.raise_for_status()
            with open(filepath, 'wb') as f:
                f.write(response.content)
        return filepath
    except Exception as e:
        print(f"[Image Download Error] {url}: {e}")
        return None

#def transform(raw_listings, car_brands):
def transform_cars():
    # TEMPORARY for transforming from json file
    with open('data/raw/listings.json', 'r') as f:
        raw_listings = json.load(f)
    with open('data/raw/brands.json', 'r') as f:
        car_brands = json.load(f)
    transformed = []
    for car in raw_listings:
        title = car.get('title', '')
        brand = extract_brand(title, car_brands)
        year = extract_year(title)
        model = extract_model(title, brand)

        raw_price = car.get('price', '')

        normalized = raw_price.replace('₱', '').replace('P', '').replace(',', '').strip()
        
        normalized = normalized.replace('–', '-')

        if normalized.upper() == 'PRICE ON REQUEST':
            price = None
        elif normalized.isdigit():
            price = int(normalized)
        elif '-' in normalized:
            parts = [p.strip() for p in normalized.split('-')]
            nums = [int(p) for p in parts if p.isdigit()]
            price = sum(nums) // len(nums) if nums else None
        else:
            price = None

        image_url = car.get('image_url')
        local_image_path = download_image(image_url) if image_url else ""

        transmission = car.get('transmission')
        fuel_type = car.get('fuel_type')
        mileage = car.get('mileage', 'Not applicable')
        location = car.get('location', '')

        if car['condition'] == 'New':
            year, trans, fuel, location = fetch_new_car_details(car['link'])
            if "Automatic" in trans and "Manual" in trans:
                transmission = "Automatic/Manual"
            else:
                transmission = transmission or trans
            if "Diesel" in fuel and "Gasoline" in fuel:
                fuel_type = "Diesel/Gasoline"
            elif "Hybrid" in fuel and "Electric" in fuel:
                fuel_type = "Hybrid/Electric"
            else:
                fuel_type = fuel_type or fuel
            mileage = 'Not applicable'
        else:
            mileage = mileage.replace('km', '').replace(',', '').strip()

        transformed.append({
            'title': title,
            'price': price,
            'link': car.get('link', ''),
            'image_url': image_url,
            'local_image_path': local_image_path,
            'brand': brand or '',
            'model': model or '',
            'year': year or '',
            'transmission': transmission or '',
            'mileage': mileage,
            'fuel_type': fuel_type or '',
            'condition': car.get('condition', ''),
            'location': location
        })

    return transformed

def extract_brand(title, car_brands):
    for brand in car_brands:
        if brand.lower() in title.lower():
            return brand
    return None

def extract_year(title):
    match = re.search(r'\b(20\d{2})\b', title)
    if match:
        return match.group(1)
    return None

def extract_model(title, brand):
    if brand:
        # Remove brand
        pattern = re.compile(re.escape(brand), re.IGNORECASE)
        model = pattern.sub('', title).strip()
        
        # Remove 4-digit year (e.g., 2010–2025)
        model = re.sub(r'\b(19|20)\d{2}\b', '', model).strip()
        
        # Clean up extra spaces
        model = re.sub(r'\s+', ' ', model)
        return model
    return title

def fetch_new_car_details(url):
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        year = None
        title_tag = soup.select_one("header h1")
        if title_tag:
            title_text = title_tag.get_text(strip=True)
            match = re.search(r"\b(19|20)\d{2}\b", title_text)
            if match:
                year = match.group(0)

        transmission = None
        fuel_type = None
        specs_rows = soup.select("#specs-table-tab tr")
        for row in specs_rows:
            cols = row.find_all('td')
            if len(cols) != 2:
                continue
            label = cols[0].get_text(strip=True)
            value = cols[1].get_text(strip=True)
            if 'Transmission' in label:
                transmission = value
            elif 'Fuel Type' in label or 'Energy Source' in label:
                fuel_type = value

        location = "Not specified"
        dealer_article = soup.select_one("article.dealer-listing")
        if dealer_article:
            dealer_details = dealer_article.select_one("div.dealer-details")
            if dealer_details:
                location_tag = dealer_details.find("p")
                if location_tag:
                    location = location_tag.get_text(strip=True)


        return year, transmission, fuel_type, location
    except Exception as e:
        print(f"[ERROR] Failed to fetch details from {url}: {e}")
        return None, None, None, None

def transform_news():
    with open('data/raw/news.json', 'r') as f:
        raw_news = json.load(f)

    transformed = []
    for news in raw_news:
        category = news.get('category', '')

        if category == 'News':
            title = news.get('title', '')
            title = title.strip()
            link = news.get('link', '')
            image_url = news.get('image_url', '')
            local_image_path = download_image(image_url) if image_url else ""
            author = news.get('author', '')
            date = news.get('date', '')
            intro = news.get('intro', '')
            intro = intro.replace('\n', ' ').strip()

            transformed.append({
                'title': title,
                'link': link,
                'image_url': image_url,
                'local_image_path': local_image_path,
                'author': author,
                'date': date,
                'intro': intro
            })

    return transformed