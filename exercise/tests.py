from django.test import TestCase

# Create your tests here.
class randomTestCase(TestCase):
    def sample_test_case(self):
        response = self.client.get(url)
        error404 = False
        if(response.status_code == 404):
            error404 = True
        self.assertIs(error404, False)