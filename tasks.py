from celery import shared_task

from Bot import Scraper
from main import RaceData, RaceScraper


@shared_task
def run_race_scraper():
    scraper = RaceScraper()
    scraper.run()
    # Example usage
    csv_file = "df_races_data.csv"
    race_data = RaceData(csv_file)

    random_record = race_data.select_random_record()
    random_race_url, random_date = race_data.get_random_race_url_and_date(random_record)

    # scraper = Scraper(random_race_url)
    scraper = Scraper(
        f"https://www.swiftbet.com.au/racing/all/{random_date}", random_race_url
    )
    scraper.run()
    return "Scraped Done!!!!"
