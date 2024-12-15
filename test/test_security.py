import unittest
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
app_path = '/Users/shahzadshabeer/Sipify-Smart-Coaster/Server/SipifyTestApp'
sys.path.append(app_path)

from app import app  

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
        # Ensure routes are protected with authentication
        response = self.app.get('/barista_mode')
        self.assertEqual(response.status_code, 404)  # Update to 401 if route is restricted

    def test_csrf_protection(self):
        # Test CSRF protection on '/get_drink_and_temperature'
        response = self.app.post(
            '/get_drink_and_temperature',
            data={'selected': 'coffee', 'input_temperature': '60'}
        )
        self.assertEqual(response.status_code, 403)  # Ensure CSRF token is required

    def test_method_restrictions(self):
        # Ensure '/get_drink_and_temperature' allows only POST
        response = self.app.get('/get_drink_and_temperature')  # Using GET instead of POST
        self.assertEqual(response.status_code, 405)  # Expect Method Not Allowed

    def test_security_headers(self):
        # Check for essential security headers in the response
        response = self.app.get('/')
        self.assertIn('Strict-Transport-Security', response.headers)
        self.assertIn('Content-Security-Policy', response.headers)
        self.assertIn('X-Content-Type-Options', response.headers)

  

    def test_session_security(self):
        # Check for secure session cookies
        response = self.app.get('/')
        self.assertIn('Set-Cookie', response.headers)
        cookie = response.headers.get('Set-Cookie')
        self.assertIn('HttpOnly', cookie)
        self.assertIn('Secure', cookie)

if __name__ == "__main__":
    unittest.main()
