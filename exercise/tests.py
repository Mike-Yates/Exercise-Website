from django.test import TestCase
from django.urls import reverse

def create_post(blog_post, blog_user):
    return Blog.objects.create(blog_post=blog_post, blog_user=blog_user)

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

    def test_blog_working(self):
        """returns true if the user is and their comment is noted"""
        blog_user = 'Admin'
        blog_post = 'This worked'
        num_before_adding = Blog.objects.all().count()
        create_post(blog_post, blog_user)
        num_after_adding = Blog.objects.all().count()
        self.assertEqual(num_after_adding - 1, num_before_adding)

    def test_blog_text(self):
        ''' Testing to see if the webpage has the text of a newly entered blog '''
        blog_user = 'Admin'
        blog_post = 'This worked round 2'
        create_post(blog_post, blog_user)
        response = self.client.get(reverse('exercise:blog'))
        self.assertContains(response, "This worked round 2")


