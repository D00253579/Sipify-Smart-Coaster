from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class BaristaModeTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            print("Setting up ChromeDriver...")
            # Set up ChromeDriver with Service
            service = Service("/Users/shahzadshabeer/Downloads/chromedriver-mac-arm64/chromedriver")
            options = Options()
            cls.driver = webdriver.Chrome(service=service, options=options)
            cls.driver.maximize_window()
        except Exception as e:
            print(f"Error setting up ChromeDriver: {e}")
            raise

    def test_page_load(self):
        try:
            print("Running test_page_load...")
            self.driver.get("https://www.sipify.site/barista_mode")
            WebDriverWait(self.driver, 10).until(EC.title_contains("Barista Mode"))
            self.assertIn("Barista Mode", self.driver.title)
        except Exception as e:
            print(f"Error in test_page_load: {e}")
            raise

    def test_no_coffee_data_message(self):
        try:
            print("Running test_no_coffee_data_message...")
            self.driver.get("https://www.sipify.site/barista_mode")
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "no_coffee_data")))
            no_coffee_message = self.driver.find_element(By.ID, "no_coffee_data")
            self.assertTrue(no_coffee_message.is_displayed())
            self.assertIn("No coffee cup detected", no_coffee_message.text)
        except Exception as e:
            print(f"Error in test_no_coffee_data_message: {e}")
            raise

    def test_coffee_data_display(self):
        try:
            print("Running test_coffee_data_display...")
            self.driver.get("https://www.sipify.site/barista_mode")
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "show_coffee_data")))
            coffee_data = self.driver.find_element(By.ID, "show_coffee_data")
            self.assertTrue(coffee_data.is_displayed())
        except Exception as e:
            print(f"Error in test_coffee_data_display: {e}")
            raise

    @classmethod
    def tearDownClass(cls):
        try:
            print("Tearing down driver...")
            cls.driver.quit()
        except Exception as e:
            print(f"Error in tearDownClass: {e}")

if __name__ == "__main__":
    unittest.main(verbosity=2)
