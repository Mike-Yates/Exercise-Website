from django.db import models

# Use this to create items needed for each user.
# The stuff in here will be used by all user, so you need to create it abstractly.
# The only difference is when you're saving/fetching it, you need to do it based on the username (which is unique)
# do some quick youtube video on how to save things for specific user in django an it should pop up easily.
