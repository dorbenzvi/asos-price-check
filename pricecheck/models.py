from django.db import models
from django.contrib.auth.models import User

class Alert(models.Model):
    id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=264)
    product_url = models.URLField()
    product_price = models.FloatField()
    user_Email = models.EmailField()
    product_img = models.URLField()
    def __str__(self):
        return self.product_name


class Users(models.Model):
    user_id = models.IntegerField(primary_key=True, auto_created=True)
    user_email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=50)

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    User._meta.get_field('email')._unique = True

    def __str__(self):
        return self.user.username