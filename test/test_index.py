from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import unittest

class SipifyHomePageTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the path to chromedriver and initialize the Service
        service = Service("/Users/shahzadshabeer/Downloads/chromedriver-mac-arm64/chromedriver")
        cls.driver = webdriver.Chrome(service=service)

    def test_page_load(self):
        # Open the site URL
        self.driver.get("https://www.sipify.site")
        # Check if page title contains 'Sipify The Smart Coaster'
        self.assertIn("Sipify The Smart Coaster", self.driver.title)

    def test_logo_display(self):
        # Check if logo image is displayed
        logo = self.driver.find_element(By.XPATH, '//img[@alt="Sipify Logo Image"]')
        self.assertTrue(logo.is_displayed(), "Logo is not displayed")

    def test_continue_button(self):
        # Check if the 'Continue' button is present and functional
        continue_button = self.driver.find_element(By.XPATH, '//button[@id="loading_button"]')
        self.assertTrue(continue_button.is_displayed(), "Continue button is not displayed")

        # Verify if the button leads to the correct URL '/drinks_selection'
        continue_button.click()
        self.assertEqual(self.driver.current_url, "https://www.sipify.site/drinks_selection")

    def test_background_images(self):
        # Check if the background images are displayed
        background_image1 = self.driver.find_element(By.XPATH, '//img[@alt="coffee background image"]')
        background_image2 = self.driver.find_element(By.XPATH, '//img[@alt="coffee background image" and @class="barista-image"]')
        
        self.assertTrue(background_image1.is_displayed(), "First background image is not displayed")
        self.assertTrue(background_image2.is_displayed(), "Second background image is not displayed")

    @classmethod
    def tearDownClass(cls):
        # Quit the driver after tests
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
