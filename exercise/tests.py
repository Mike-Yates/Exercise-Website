from django.test import TestCase

# Create your tests here.
class Test(TestCase):
    def test_case(self):
        """
        Sample test to see if the url 404s or not
        """
        response = self.client.get(url)
        error404 = False
        if(response.status_code == 404):
            error404 = True
        self.assertIs(error404, False)