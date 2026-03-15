from app.etl.extract import extract_cars, extract_news
from app.etl.transform import transform_cars, transform_news
from app.etl.load import load_cars, load_news

def run_etl():
    #listings, brands = extract(max_pages=1)
    #transformed = transform(listings, list(brands))
    extract_cars(max_pages=1)
    extract_news()
    transformed_cars = transform_cars()
    load_cars(transformed_cars)

    transformed_news = transform_news()
    load_news(transformed_news)
