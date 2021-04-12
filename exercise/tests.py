from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from exercise.models import *
from django.utils import timezone


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

    def test_response_status_dev_site(self):
        '''
        Test case to make sure dev site it running. 
        '''
        url = 'https://exercisegamificationdev.herokuapp.com/'
        response = self.client.get(url)
        error404 = False
        if (response.status_code == 404):
            error404 = True
        self.assertIs(error404, False)

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

    def test_exercise_test(self):
        """returns true if an exercise is added and is displayed on the user's page"""
        reps = 3
        sets = 3
        exercise_name = 'pushup'
        user = User.objects.create_user(
            'Jerry', 'lennon@thebeatles.com', 'johnpassword')
        x = Exercise.objects.create(
            user=user, exercise_name=exercise_name, reps=reps, sets=sets)
        self.client.force_login(User.objects.get_or_create(username='Jerry')[0])
        response = self.client.get(reverse('exercise:exerciselogging'))
        self.assertContains(response, exercise_name)
        self.assertContains(response, sets)
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

    def test_sportXP_zero_defaultValue(self):
        """returns True if all sportXP values are defaulted to 0"""
        user = User.objects.create_user(
            'testUser', 'tester@outlook.com', 'testUserpassword'
        )
        x = SportsXP.objects.create(user=user)
        zero = 0
        if (x.basketball > zero):
            zero = x.basketball
        if (x.cross_training > zero):
            zero = x.cross_training
        if (x.cardio > zero):
            zero = x.cardio
        if (x.strength_training > zero):
            zero = x.strength_training
        if (x.climbing > zero):
            zero = x.climbing
        if (x.soccer > zero):
            zero = x.soccer
        if (x.american_football > zero):
            zero = x.american_football
        if (x.dance > zero):
            zero = x.dance
        if (x.gymnastics > zero):
            zero = x.gymnastics
        if (x.hiking > zero):
            zero = x.hiking
        if (x.swimming > zero):
            zero = x.swimming
        if (x.yoga > zero):
            zero = x.yoga
        self.assertEqual(0, zero)
        user.delete()

    def test_SportXP_can_change(self):
        """returns True if sportXP values can change from default 0 value"""
        user = User.objects.create_user(
            'testUser', 'tester@outlook.com', 'testUserpassword'
        )
        x = SportsXP.objects.create(user=user)
        x.cardio = 3
        self.assertEqual(3, x.cardio)
        user.delete()

    def test_SportsXP_tied_to_user(self):
        """returns True if sportXP value changes are tied to a single user"""
        user = User.objects.create_user(
            'testUser', 'tester@outlook.com', 'testUserpassword'
        )
        x = SportsXP.objects.create(user=user)

        second_User = User.objects.create_user(
            'second', 'secondUser@outlook.com', 'testSecond'
        )
        y = SportsXP.objects.create(user=second_User)
        y.swimming = 3
        self.assertEqual(x.swimming, 0)
        user.delete()
        second_User.delete()

    def test_timestamp_is_noted_with_SportsXP(self):
        time = timezone.now()
        user = User.objects.create_user(
            'testUser', 'tester@outlook.com', 'testUserpassword'
        )
        x = SportsXP.objects.create(user=user)
        self.assertIs(time < x.timestamp, True)
        user.delete()

    def test_bmi_shows_proper_bmi(self):
        user = User.objects.create_user(
            'Joe', 'lennon@thebeatles.com', 'johnpassword')
        x = Bmi.objects.create(
            user=user, height_feet=6, height_inches=0, weight_pounds=200, user_bmi=27)
        self.client.force_login(User.objects.get_or_create(username='Joe')[0])
        response = self.client.get(reverse('exercise:bmidisplay'))
        self.assertContains(response, 27)
        user.delete()

    def test_bmi_added_to_queryset(self):
        """returns true if an exercise is added"""
        user = User.objects.create_user(
            'Joe', 'lennon@thebeatles.com', 'johnpassword')
        num_before_adding = Bmi.objects.all().count()
        x = Bmi.objects.create(
            user=user, height_feet=6, height_inches=0, weight_pounds=200, user_bmi=27)
        num_after_adding = Bmi.objects.all().count()
        self.assertEqual(num_after_adding - 1, num_before_adding)
        user.delete()

    def test_bmi_display_user_specific(self):
        user1 = User.objects.create_user(
            'test1', 'lennon@thebeatles.com', 'johnpassword')
        user2 = User.objects.create_user(
            'test2', 'lennon@thebeatles.com', 'johnpassword')
        x = Bmi.objects.create(
            user=user1, height_feet=6, height_inches=0, weight_pounds=200, user_bmi=27)
        self.client.force_login(User.objects.get_or_create(username='test2')[0])
        response = self.client.get(reverse('exercise:bmidisplay'))
        self.assertNotContains(response, 27)
        user1.delete()
        user2.delete()

    def test_no_timestamp_dependence_SportXP(self):
        user = User.objects.create_user(
            'testUser','tester@outlook.com', 'testUserpassword'
        )
        x = SportsXP.objects.create(user = user)
        userSecond = User.objects.create_user(
            'testUserSecond','testerSecond@outlook.com', 'testUserpasswordSecond'
        )
        y = SportsXP.objects.create(user = userSecond)
        self.assertIs(x.timestamp != y.timestamp, True)
        user.delete()
        userSecond.delete()

    
    def test_SportsXP_reset(self):
        user = User.objects.create_user(
            'testUser','tester@outlook.com', 'testUserpassword'
        )
        x = SportsXP.objects.create(user = user)
        x.swimming = 3
        x.swimming = 0
        self.assertEqual(x.swimming, 0)
        user.delete()

    def test_SportsXP_reset_no_dependence(self):
        user = User.objects.create_user(
            'testUser','tester@outlook.com', 'testUserpassword'
        )
        x = SportsXP.objects.create(user = user)
        userSecond = User.objects.create_user(
            'testUserSecond','testerSecond@outlook.com', 'testUserpasswordSecond'
        )
        y = SportsXP.objects.create(user = userSecond)
        x.swimming = 3
        y.swimming = 3
        x.swimming = 0
        self.assertEqual(y.swimming, 3)
        user.delete()
        userSecond.delete()