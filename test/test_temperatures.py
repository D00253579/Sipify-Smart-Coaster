from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import unittest

class TestTemperaturesPage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the path to chromedriver and initialize the Service
        service = Service("/Users/shahzadshabeer/Downloads/chromedriver-mac-arm64/chromedriver")
        cls.driver = webdriver.Chrome(service=service)

    def test_page_load(self):
        # Test if the temperatures page loads successfully
        self.driver.get("https://www.sipify.site/temperatures")
        self.assertIn("Temperatures", self.driver.title)

    def test_table_display(self):
        # Test if the table containing drink temperatures is present
        self.driver.get("https://www.sipify.site/temperatures")
        table = self.driver.find_element(By.CSS_SELECTOR, "table.table")
        self.assertTrue(table.is_displayed())
        
    def test_table_data(self):
        # Check if each drink's name, minimum temperature, and maximum temperature are displayed
        self.driver.get("https://www.sipify.site/temperatures")
        rows = self.driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
        self.assertGreater(len(rows), 0)  # Ensure at least one drink is listed
        
        # Check if each row contains drink name, min and max temperature
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            self.assertEqual(len(columns), 3)  # Each row should have 3 columns

   

    @classmethod
    def tearDownClass(cls):
        # Quit the driver after tests
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
