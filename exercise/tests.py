from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from exercise.models import Blog, Exercise


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
        if (response.status_code == 404):
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

    def test_exercise_logging_creation(self):
        """returns true if an exercise is added"""
        reps = 3
        sets = 3
        exercise_name = 'pushup'
        user = User.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword')
        num_before_adding = Exercise.objects.all().count()
        x = Exercise.objects.create(
            user=user, exercise_name=exercise_name, reps=reps, sets=3)
        num_after_adding = Exercise.objects.all().count()
        self.assertEqual(num_after_adding - 1, num_before_adding)
        user.delete()

    def test_exercise_logging_adds_to_user(self):
        """returns true if an exercise is added to that user"""
        reps = 3
        sets = 3
        exercise_name = 'pushup'
        user = User.objects.create_user(
            'james', 'lennon@thebeatles.com', 'johnpassword')
        user.exercise = Exercise()
        num_before_adding = getattr(user.exercise, 'reps')
        user.exercise.user_id = User.objects.get(
            username="james").pk
        user.exercise.reps = reps
        user.exercise.save()
        num_after_adding = getattr(user.exercise, 'reps')
        print(num_before_adding, num_after_adding)
        self.assertEqual(num_after_adding - reps, num_before_adding)
        user.delete()

    def test_blog_text(self):
        ''' Testing to see if the webpage has the text of a newly entered blog '''
        blog_user = 'Admin'
        blog_post = 'This worked round 2'
        create_post(blog_post, blog_user)
        response = self.client.get(reverse('exercise:blog'))
        self.assertContains(response, "This worked round 2")


    def test_blog_text2(self):
        ''' Testing to see if the webpage has the text of two newly entered blogs,
        and that the blog user's name is also listed '''
        blog_user = 'Admin'
        blog_post = 'This worked'
        blog_user2 = 'Admin2'
        blog_post2 = 'This worked round 2'
        create_post(blog_post, blog_user)
        create_post(blog_post2, blog_user2)

        response = self.client.get(reverse('exercise:blog'))
        self.assertContains(response, "This worked")
        self.assertContains(response, "This worked round 2")
        self.assertContains(response, "Admin")
        self.assertContains(response, "Admin2")

