from django.test import TestCase


class RandomTestCase(TestCase):
    '''
    Test class used to hold test for the site
    '''

    def test_response_status(self):
        '''
        Example dummy test case to make sure travis is working correctly. 
        '''
        url = 'https://exercisegamification.herokuapp.com/'
        response = self.client.get(url)
        error404 = False
        if(response.status_code == 404):
            error404 = True
        self.assertIs(error404, False)

    # Write some more test cases here
