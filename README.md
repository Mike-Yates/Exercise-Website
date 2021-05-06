# **Exercise Gamification**

## Creating a new account!
#### Once you’ve made it to the first time login page, enter your name and bio. After submitting this, you will be taken to the ‘home’ page, displaying your user name and a partially filled XP bar; you may increase your different activity levels by selecting the blank text box just beneath the partially filled XP bar under your user name. Once an activity is selected from the dropdown of activities (after clicking the blank text box), you may hit the ‘submit’ button to record your submission for that activity.

### The basics of our app: 
Navigate to any page by clicking its name displayed on the header of every page. 
On the sports page, click any of the sports graphics to see an example workout matching that exercise. 
The exercise page allows you to keep a history of what exercises you do. 
The friends feature allows you to see what exercises your friends are doing (displayed on the ‘exercise’ page)
The bmi page allows you to calculate your bmi, and keeps track of your submissions to track your progress! (displayed on a graph at the bottom of the page) 
The youtube page lets you quickly search for exercise videos 


### Instructions for creators:

    To be able to use this project you have to create a virtual enviroment.

    1. Install Python3 to your system. (https://www.python.org/downloads/)
    2. Clone the repository.
    3. Create a virtual environment:
        Windows: python -m venv env
        MacOS: python3 -m venv env
    4. Start the virtual environment:
        Windows: .\env\Scripts\activate
        MacOS: source env/bin/activate
        - Note: If you are on the Windows Subsystem for Linux (BASH) use: source env/Scripts/activate
    5. Install from the requirements file
        Windows: python -m pip install -r requirements.txt
        MacOS: python3 -m pip install -r requirements.txt
   
    To start the local server run:
        Windows: python manage.py runserver
        MacOS: python3 manage.py runserver

    To close your environment run the command:
        Windows/MacOS: deactivate

### Tips:
    To be able to run the project locally, you need to recreate the ".env" file with the appropriate database instruction. You need the following information in the ".env" file
       1. Create a ".env" file in the same directory as the "manage.py" file
       2. Add the following information to the ".env" file
            SECRET_KEY='...'
            ENGINE='...
            NAME='...'
            PERSON='...'
            PASSWORD='...'
            HOST='...'
            YOUTUBE_API_KEY='...'
            DEBUG=<True or False>

       3. Make sure to include the same information in your production server
       4. Create a superuser with the information so you can login to the database
       5. Deploy your site and visit the "/admin" to login. 
   
### Resources:
    Here are resources that were refered to in the development of this project:
    1. https://github.com/joke2k/django-environ
    2. https://www.youtube.com/watch?v=GMbVzl_aLxM
    3. https://whizzoe.medium.com/in-5-mins-set-up-google-login-to-sign-up-users-on-django-e71d5c38f5d5
    4. https://docs.djangoproject.com/en/3.1/intro/tutorial01/
    5. https://stackoverflow.com/questions/15409366/django-socialapp-matching-query-does-not-exist
    6. https://gist.github.com/bennylope/2999704
    7. https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
    7. https://codesource.io/ci-cd-with-github-travis-ci-and-heroku/
    8. https://docs.travis-ci.com/user/deployment/heroku/#deploying-specific-branches
    9. https://docs.djangoproject.com/en/3.0/ref/contrib/messages/#using-messages-in-views-and-templates
    10. https://www.youtube.com/watch?v=tUqUdu0Sjyc
    11. https://github.com/revsys/django-friendship
    12. https://pypi.org/project/django-friendship/
    13. https://www.youtube.com/watch?v=lc2KvFbbfAQ
    
### Contributions:
    If you are willing to contribute to this projects, please fork the repo and make a pull request once you are done. We will take a look and see what we can do with it.
