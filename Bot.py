import os

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WebDriverManager:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        # options.add_argument('--headless')  # Uncomment for headless mode
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")
        self.driver = None

    def init_driver(self):
        if not self.driver:
            self.driver = webdriver.Chrome(options=self.options)
            self.driver.maximize_window()
        return self.driver

    def wait_for_element(self, timeout, by_type, selector):
        try:
            element_present = EC.presence_of_element_located((by_type, selector))
            WebDriverWait(self.driver, timeout).until(element_present)
            return self.driver.find_element(by_type, selector)
        except TimeoutException:
            print(f"Timed out waiting for element: {selector}")
            return None

    def navigate_to_url(self, url):
        self.driver.get(url)

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None


class Scraper:
    def __init__(self, url, second_page_url):
        self.driver_manager = WebDriverManager()
        self.url = url
        self.second_page_url = second_page_url
        self.data = []
        self.class_name = (
            "css-1c8uam-ListItem-ListItem-ListItem-RaceSelectionsListItem-"
            "RaceSelectionsListItem-RaceSelectionsListItem-RaceSelectionsListItem"
        )

    def scrape_data(self):
        driver = self.driver_manager.init_driver()
        driver.get(self.url)

        try:
            # Wait for the specific link and click it
            link = self.driver_manager.wait_for_element(
                20,
                By.CSS_SELECTOR,
                f'a[href="{self.second_page_url}"]',
            )

            if link:
                link.click()
                # time.sleep(10)
                print("Link clicked successfully!")
            else:
                print("Link not found!")
            # Wait for the next page to load
            try:
                WebDriverWait(self.driver_manager.driver, 20).until(
                    EC.presence_of_element_located(
                        (
                            By.CLASS_NAME,
                            self.class_name,
                        )
                    )
                )

                # Extract page source after the page has loaded
                html = self.driver_manager.driver.page_source
                soup = BeautifulSoup(html, "html.parser")

                # Find the 'ul' element with the desired class
                ul = soup.find("ul", {"class": "en9z9v58"})
                if ul:
                    for li in ul.find_all(
                        "li",
                        {"class": self.class_name},
                    ):
                        title = li.find("div", {"class": "e3trgs57"})
                        Fixed_W = li.find("div", {"class": "egik0gw5"})

                        # Check if Fixed_W exists before finding the next div
                        Fixed_P = (
                            Fixed_W.find_next("div", {"class": "egik0gw5"})
                            if Fixed_W
                            else None
                        )

                        # Create a dictionary with the text content
                        self.data.append(
                            {
                                "Title": title.text if title else None,
                                "Fixed_W": (
                                    Fixed_W.text.replace("FAV", "").strip()
                                    if Fixed_W
                                    else None
                                ),
                                "Fixed_P": (
                                    Fixed_P.text.replace("FAV", "").strip()
                                    if Fixed_P
                                    else None
                                ),
                            }
                        )

                else:
                    print("The 'ul' element was not found on the page.")

            except TimeoutException:
                print("Loading the page took too long or the element was not found.")

        except NoSuchElementException as e:
            print(f"Element not found during scraping: {e}")
        finally:
            # Optional: Close driver if desired, or leave open for future interactions
            # self.driver_manager.driver.quit()
            pass

    def save_data(self, filename="df_performed_bets.csv"):
        """Save the collected race data into a CSV file."""
        df_races_data = pd.DataFrame(self.data)
        # Specify the folder where you want to save the CSV
        folder_path = "CSV"
        # Create the folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)
        # Construct the full file path
        full_path = os.path.join(folder_path, filename)
        # Save the DataFrame to the specified path
        df_races_data.to_csv(full_path, index=False)

    def run(self):
        self.scrape_data()
        self.save_data()
        self.driver_manager.close_driver()


if __name__ == "__main__":
    url = "https://www.swiftbet.com.au/racing"
    s_url = (
        "https://www.swiftbet.com.au/racing/gallops/caulfield/race-1-1854365-1078631"
    )
    second_page_url = s_url  # please change URL
    scraper = Scraper(url, second_page_url)
    scraper.run()
