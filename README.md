# **Exercise Gamification**

### Instructions:

    To be able to use this project you have to create a virtual enviroment.

    1. Install Python3 to your system. (https://www.python.org/downloads/)
    2. Clone the repository.
    3. Create a virtual environment:
        Windows: py -m venv env
        MacOS: python3 -m venv env
    4. Start the virtual environment:
        Windows: .\env\Scripts\activate
        MacOS: source env/bin/activate
        - Note: If you are on the Windows Subsystem for Linux (BASH) use: source env/Scripts/activate
    5. Install from the requirements file
        Windows: python -m pip install -r requirements.txt
        MacOS: python3 -m pip install -r requirements.txt
   
    To start the local server run:
        Windows: py manage.py runserver
        MacOS: python3 manage.py runserver

    To close your environment run the command:
        Windows/MacOS: deactivate

### Tips:
    To be able to run the project locally, you need to recreate the ".env" file with the appropriate database instruction. You need the following information in the ".env" file
       1. Create a ".env" file in the same directory as the "manage.py" file
       2. Add the following information to the ".env" file
           - SECRET_KEY='<insert secret key>'
           - DATABASE_URL='<insert url to postgres database>'
           - DEBUG='<FALSE for production, TRUE for development>'
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
    7. 
    
### Contributions:
    If you are willing to contribute to this projects, please fork the repo and make a pull request once you are done. We will take a look and see what we can do with it.
