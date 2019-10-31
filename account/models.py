from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    StudentID = models.CharField(max_length=10, null=True)
    phone = models.CharField(max_length=20, null=True)

    is_active = models.BooleanField(default=False)
    code = models.CharField(max_length=20, verbose_name='验证码', blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    school = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    aboutme = models.TextField(blank=True)
    photo = models.ImageField(upload_to='images/%Y/%m/%d')


    def __str__(self):
        return "user:{}".format(self.user.username)



