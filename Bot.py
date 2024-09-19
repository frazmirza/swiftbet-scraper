# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# import time
# import csv
#
# def init_driver():
#     options = webdriver.ChromeOptions()
#     # options.add_argument('--headless')
#     options.add_argument('--disable-gpu')
#     options.add_argument('--no-sandbox')
#     driver = webdriver.Chrome(options=options)
#     driver.maximize_window()
#     return driver
#
# def wait_for_element(driver, timeout, by_type, selector):
#     try:
#         element_present = EC.presence_of_element_located((by_type, selector))
#         WebDriverWait(driver, timeout).until(element_present)
#         return driver.find_element(by_type, selector)
#     except TimeoutException:
#         print(f"Timed out waiting for element: {selector}")
#         return None
#
# def navigate_to_url(driver, url):
#     driver.get(url)
#
#
# def scrape_data(driver):
#     try:
#         # Wait for the link with the specific href to appear
#         link = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR,
#                                             'a[href="https://swiftbet.com.au//racing/greyhounds/ascot-park/race-1-1850175-1078215"]'))
#         )
#
#         # Click the link once it's found
#         link.click()
#         print("Link clicked successfully!")
#
#         # Optionally, retrieve all links on the page after the click
#         links = driver.find_elements(By.TAG_NAME, 'a')
#         return {"clicked_link": link.get_attribute('href'), "all_links": [l.get_attribute('href') for l in links]}
#
#     except Exception as e:
#         print(f"Error during scraping: {e}")
#         return None
#
# def save_to_csv(data, filename="scraped_data.csv"):
#     with open(filename, mode="w", newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=data.keys())
#         writer.writeheader()
#         writer.writerow(data)
#
# def close_driver(driver):
#     driver.quit()
#
# def main(url):
#     driver = init_driver()
#     navigate_to_url(driver, url)
#     data = scrape_data(driver)
#     time.sleep(50)
#     # if data:
#     #     save_to_csv(data)
#     close_driver(driver)
#
# if __name__ == "__main__":
#     url = "https://www.swiftbet.com.au/racing"
#     main(url)


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import csv


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
        self.data = None

    def scrape_data(self):
        driver = self.driver_manager.init_driver()
        driver.get(self.url)

        try:
            # Wait for the specific link (modify selector if needed)
            link = self.driver_manager.wait_for_element(
                10,
                By.CSS_SELECTOR,
                f'a[href="{self.second_page_url}"]',
                # 'a[href="https://swiftbet.com.au//racing/greyhounds/ascot-park/race-1-1850175-1078215"]',
            )

            # Click the link
            link.click()
            print("Link clicked successfully!")

            # Optionally, retrieve all links on the page after the click
            links = driver.find_elements(By.TAG_NAME, "a")
            self.data = {
                "clicked_link": link.get_attribute("href"),
                "all_links": [l.get_attribute("href") for l in links],
            }

        except Exception as e:
            print(f"Error during scraping: {e}")

    def save_to_csv(self, filename="scraped_data.csv"):
        if self.data:
            with open(filename, mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.data.keys())
                writer.writeheader()
                writer.writerow(self.data)

    def run(self):
        self.scrape_data()
        # self.save_to_csv()
        self.driver_manager.close_driver()


if __name__ == "__main__":
    url = "https://www.swiftbet.com.au/racing"
    scraper = Scraper(url)
    scraper.run()
