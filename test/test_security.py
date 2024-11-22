import unittest
import os
import sys

# Add the path to your app to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
app_path = '/Users/shahzadshabeer/Sipify-Smart-Coaster/Server/SipifyTestApp'
sys.path.append(app_path)

from app import app  # Import your Flask app



class TestSecurity(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_sql_injection(self):
        # Test SQL injection on '/get_drink_and_temperature'
        response = self.app.post(
            '/get_drink_and_temperature',
            data={'selected': "coffee'; DROP TABLE users;--", 'input_temperature': '60'}
        )
        self.assertNotIn('error', response.data.decode())
        self.assertNotIn("DROP TABLE", response.data.decode())

    def test_input_sanitization(self):
        # Test input sanitization for potential XSS
        response = self.app.post(
            '/get_drink_and_temperature',
            data={'selected': "<script>alert('XSS')</script>", 'input_temperature': '60'}
        )
        self.assertNotIn('<script>', response.data.decode())
        self.assertNotIn('alert', response.data.decode())

def test_authentication_required(self):
    response = self.app.get('/barista_mode')
    self.assertEqual(response.status_code, 404)  

if __name__ == "__main__":
    unittest.main()
