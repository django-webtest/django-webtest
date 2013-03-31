import django

if django.get_version() >= "1.5":
    from django.contrib.auth.models import AbstractBaseUser
    from django.db import models


    class CustomUser(AbstractBaseUser):
        email = models.EmailField(
            max_length=255,
            unique=True,
            db_index=True,
        )
        USERNAME_FIELD = 'email'
