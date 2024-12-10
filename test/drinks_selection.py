from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import unittest

class DrinkSelectionTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the path to chromedriver and initialize the Service
        service = Service("/Users/shahzadshabeer/Downloads/chromedriver-mac-arm64/chromedriver")
        cls.driver = webdriver.Chrome(service=service)

    def test_page_load(self):
        # Open the site URL for the Drink Selection page
        self.driver.get("https://www.sipify.site/drinks_selection")
        # Check if page title contains 'Drink Selection'
        self.assertIn("Drink Selection", self.driver.title)

    def test_temperature_input_field(self):
        # Check if the temperature input field is present and visible
        temperature_input = self.driver.find_element(By.ID, "current_temperature")
        self.assertTrue(temperature_input.is_displayed(), "Temperature input field is not displayed")

    def test_drink_selection_radio_buttons(self):
        # Verify that each drink option is displayed
        drinks = self.driver.find_elements(By.NAME, "selected")
        self.assertGreater(len(drinks), 0, "No drinks options available")
        
        for drink in drinks:
            self.assertTrue(drink.is_displayed(), f"Drink option {drink.get_attribute('value')} is not displayed")
    
    def test_submit_button_functionality(self):
        # Verify if the 'Next' button is present and functional
        next_button = self.driver.find_element(By.ID, "loading_button")
        self.assertTrue(next_button.is_displayed(), "Next button is not displayed")

        # Select a drink and enter a temperature
        self.driver.find_element(By.NAME, "selected").click()
        self.driver.find_element(By.ID, "current_temperature").send_keys("25")
        
        # Click on the 'Next' button to submit the form
        next_button.click()

     

    def test_background_image(self):
        # Check if the background image is displayed
        background_image = self.driver.find_element(By.XPATH, '//img[@alt="coffee background image"]')
        self.assertTrue(background_image.is_displayed(), "Background image is not displayed")

    @classmethod
    def tearDownClass(cls):
        # Quit the driver after tests
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
