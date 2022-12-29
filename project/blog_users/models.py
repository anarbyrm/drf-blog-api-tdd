from django.contrib.auth.models import (
                        AbstractBaseUser,
                        PermissionsMixin,
                        BaseUserManager
                        )
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(max_length=225, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
