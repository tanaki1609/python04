from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, User
from django.db import models
from django.db.models import SET_NULL


class ConfirmationCode(models.Model):
    code = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True)
    valid_until = models.DateTimeField()

    def __str__(self):
        return self.code
