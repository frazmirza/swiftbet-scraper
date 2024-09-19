import pandas as pd
import random
import ast


class RaceData:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)

    def select_random_record(self):
        random_row = self.df.sample()
        return random_row.to_dict(orient="records")[0]

    def get_random_race_url_and_date(self, random_record):
        races_list = ast.literal_eval(random_record["Races"])
        random_race = random.choice(races_list)
        return random_race["Race_URL"], random_race["Race_Time"]


# Example usage
csv_file = "df_races_data.csv"
race_data = RaceData(csv_file)

random_record = race_data.select_random_record()
random_race_url, random_date = race_data.get_random_race_url_and_date(random_record)

print(random_date)
print(random_race_url)
