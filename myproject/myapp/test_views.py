import unittest
from unittest.mock import patch
from django.test import RequestFactory
from .views import fetch_and_extract_menu
import pandas as pd

class TestFetchAndExtractMenu(unittest.TestCase):
    """
    Unit tests for the fetch_and_extract_menu function in the views module.
    """

    @patch('myapp.views.fetch_menu')
    @patch('myapp.views.extract_menu')
    def test_fetch_and_extract_menu_success(self, mock_extract_menu, mock_fetch_menu):
        """
        Test the fetch_and_extract_menu function when menu data is successfully fetched and extracted.
        """
        mock_fetch_menu.return_value = {'data': {'cards': [{'groupedCard': {'cardGroupMap': {'REGULAR': {'cards': []}}}}]}}
        mock_extract_menu.return_value = pd.DataFrame({'Name': ['Dish1'], 'Price': [10], 'Category': ['Cat1'], 'Description': ['Desc1']})
        
        request = RequestFactory().get('/', {'restaurant_id': '12345'})
        response = fetch_and_extract_menu(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dish1', response.content)

    @patch('myapp.views.fetch_menu')
    def test_fetch_and_extract_menu_failure_fetch(self, mock_fetch_menu):
        """
        Test the fetch_and_extract_menu function when fetching menu data fails.
        """
        mock_fetch_menu.return_value = None

        request = RequestFactory().get('/', {'restaurant_id': '12345'})
        response = fetch_and_extract_menu(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Failed to fetch menu data.', response.content)

    @patch('myapp.views.fetch_menu')
    @patch('myapp.views.extract_menu')
    def test_fetch_and_extract_menu_failure_extract(self, mock_extract_menu, mock_fetch_menu):
        """
        Test the fetch_and_extract_menu function when extracting menu data fails.
        """
        mock_fetch_menu.return_value = {'data': {'cards': [{'groupedCard': {'cardGroupMap': {'REGULAR': {'cards': []}}}}]}}
        mock_extract_menu.return_value = None

        request = RequestFactory().get('/', {'restaurant_id': '12345'})
        response = fetch_and_extract_menu(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Failed to extract menu data.', response.content)

    def test_fetch_and_extract_menu_invalid_request_method(self):
        """
        Test the fetch_and_extract_menu function with an invalid request method.
        """
        request = RequestFactory().post('/')
        response = fetch_and_extract_menu(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid request method.', response.content)

    def test_fetch_and_extract_menu_missing_restaurant_id(self):
        """
        Test the fetch_and_extract_menu function with a missing restaurant ID.
        """
        request = RequestFactory().get('/')
        response = fetch_and_extract_menu(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please provide a restaurant ID.', response.content)

if __name__ == '__main__':
    unittest.main()
