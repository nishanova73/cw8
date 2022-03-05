from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, verbose_name='User')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Date of birth:')
    avatar = models.ImageField(null=True, blank=True, upload_to='user_pics', verbose_name='Avatar')
    about = models.TextField(max_length=500, blank=True, null=True, verbose_name='About')

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'