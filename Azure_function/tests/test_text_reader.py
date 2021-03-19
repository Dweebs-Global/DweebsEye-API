import unittest

import azure.functions as func
from text_reader import main


class TestFunction(unittest.TestCase):
    def test_no_headers(self):
        """Test case for request without the right headers or body"""
        req = func.HttpRequest(     # a mock HTTP request
            url='/api/text_reader',
            headers={},
            method='POST',
            body=None            
        )
        resp = main(req)
        self.assertEqual(
            resp.get_body(),
            b'Not valid or not specified content type in the headers.'
        )
    
    def test_no_body(self):
        """Test case for request with right headers but no body"""
        req = func.HttpRequest(     # a mock HTTP request
            url='/api/text_reader',
            method='POST',
            headers={'Content-Type': 'image/jpeg'},
            body=None            
        )
        resp = main(req)
        self.assertEqual(
            resp.get_body(),
            b'No valid image provided.'
        )
    
    def test_wrong_body(self):
        """Test case for request with right headers but wrong body"""
        req = func.HttpRequest(     # a mock HTTP request
            url='/api/text_reader',
            method='POST',
            headers={'Content-Type': 'image/jpeg'},
            body="{body:Some wrong body}"          
        )
        resp = main(req)
        self.assertEqual(
            resp.get_body(),
            b'No valid image provided.'
        )
    
    def test_wrong_method(self):
        """Test case for request with wrong method"""
        req = func.HttpRequest(     # a mock HTTP request
            url='/api/text_reader',
            method='DELETE',
            headers={'Content-Type': 'image/jpeg'},
            body=None            
        )
        resp = main(req)
        self.assertEqual(
            resp,
            None
        )
