import ast
import json
import os
import random
from datetime import datetime, timedelta

import pandas as pd
import requests

from Bot import Scraper


class RaceData:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)

    def select_random_record(self):
        random_row = self.df.sample()
        return random_row.to_dict(orient="records")[0]

    def get_random_race_url_and_date(self, random_record):
        races_list = ast.literal_eval(random_record["Races"])
        random_race = random.choice(races_list)
        return random_race["Race_URL"], random_race["Race_Time"].split(" ")[0]


class RaceScraper:
    def __init__(self, country_filter=["AU", "NZ"]):
        self.country_filter = country_filter
        self.data_list = []

    def get_date(self, days_offset=0):
        """Returns today's or tomorrow's date in 'YYYY-MM-DD' format."""
        date = (datetime.now() + timedelta(days=days_offset)).strftime("%Y-%m-%d")
        return date

    def fetch_race_data(self, date):
        """Fetch race data from the API for a specific date."""
        url = "https://api.swiftbet.com.au/api/v2/combined/meetings/races?"
        url += f"order=true&date={date}"
        print(f"Fetching data for {date} from: {url}")
        res = requests.get(url)
        return json.loads(res.text)

    def filter_and_process_data(self, json_response):
        """Filter race data by country and process race information."""
        for data in json_response.get("data", []):
            if data["country"] in self.country_filter:
                track_name = data["name"]
                races = data["races"]
                all_races = self.process_races(races)
                data_dict = {"Track_name": track_name, "Races": all_races}
                self.data_list.append(data_dict)

    def process_races(self, races):
        """Process the race information for each track."""
        all_races = []
        for index, race in enumerate(races, start=1):
            race_url = race.get("race_site_link", "")
            time_to_race_start = race.get("start_date", "")
            result_string = race.get("result_string", "")
            race_name = race.get("name", "")

            all_races.append(
                {
                    "Race_Number": f"Race {index}",
                    "Race_URL": race_url,
                    "Race_Time": time_to_race_start,
                    "Result_String": result_string,
                    "Race_Name": race_name,
                }
            )
        return all_races

    def save_data(self, filename="df_races_data.csv"):
        """Save the collected race data into a CSV file."""
        df_races_data = pd.DataFrame(self.data_list)
        # Specify the folder where you want to save the CSV
        folder_path = "CSV"
        # Create the folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)
        # Construct the full file path
        full_path = os.path.join(folder_path, filename)
        # Save the DataFrame to the specified path
        df_races_data.to_csv(full_path, index=False)

    def run(self):
        """Run the entire scraping process for both today and tomorrow."""
        for days_offset in range(2):  # 0 for today, 1 for tomorrow
            date = self.get_date(days_offset)
            json_response = self.fetch_race_data(date)
            self.filter_and_process_data(json_response)
        self.save_data()


# Main execution
if __name__ == "__main__":
    scraper = RaceScraper()
    scraper.run()

    # Example usage
    csv_file = "CSV/df_races_data.csv"
    race_data = RaceData(csv_file)

    random_record = race_data.select_random_record()
    random_race_url, random_date = race_data.get_random_race_url_and_date(random_record)

    # scraper = Scraper(random_race_url)
    scraper = Scraper(
        f"https://www.swiftbet.com.au/racing/all/{random_date}", random_race_url
    )
    scraper.run()
