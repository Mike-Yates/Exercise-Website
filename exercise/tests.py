from django.test import TestCase

# Create your tests here.
class RandomTestCase(TestCase):
    def test_case(self):
        url = 'https://exercisegamification.herokuapp.com/'
        response = self.client.get(url)
        error404 = False
        if(response.status_code == 404):
            error404 = True
        self.assertIs(error404, False)