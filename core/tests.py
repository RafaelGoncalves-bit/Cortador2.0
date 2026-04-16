from django.test import TestCase

class CortadorTest(TestCase):

    def setUp(self):
        self.resp = self.client.get('/')
    
    def test_200_response(self):
        self.assertEqual(200, self.resp.status_code)
