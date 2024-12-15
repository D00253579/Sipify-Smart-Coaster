from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager 

class DrinkHistoryPageTests(unittest.TestCase):
    
    def setUp(self):
        # Use the Service class to specify the chromedriver path
        service = Service("/Users/shahzadshabeer/Downloads/chromedriver-mac-arm64/chromedriver")
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get("https://www.sipify.site/history")  
    
    def tearDown(self):
        # Close the WebDriver after the tests
        self.driver.quit()
    
    def test_page_title(self):
        # Verify the title of the page
        self.assertEqual(self.driver.title, "Drink History")
    
    def test_table_presence(self):
        # Verify the table is present
        table = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        self.assertIsNotNone(table, "Table should be present on the page.")
    
    def test_table_headers(self):
        # Verify the table headers (Drink Name, Temperature, Notification)
        headers = self.driver.find_elements(By.CSS_SELECTOR, "table thead th")
        header_texts = [header.text for header in headers]
        self.assertIn("Drink Name", header_texts)
        self.assertIn("Temperature", header_texts)
        self.assertIn("Notification", header_texts)
    
    def test_table_data(self):
        # Check if the rows in the table are populated with drink data
        rows = self.driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        self.assertGreater(len(rows), 0, "Table should have at least one row of data.")

        # Verify that the rows have the correct number of columns 
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            self.assertEqual(len(columns), 3, "Each row should have exactly 3 columns.")
    
    def test_back_button(self):
     
        back_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "loading_button"))
        )
        self.assertIsNotNone(back_button, "Back button should be present.")
        
    
        back_button.click()
        WebDriverWait(self.driver, 10).until(EC.url_to_be("https://www.sipify.site/barista_controls"))
        self.assertEqual(self.driver.current_url, "https://www.sipify.site/barista_controls")
    
if __name__ == "__main__":
    unittest.main()
