import django

if django.VERSION >= (1, 5):
    from django.contrib.auth.models import AbstractBaseUser
    from django.db import models


    class MyCustomUser(AbstractBaseUser):
        email = models.EmailField(
            max_length=255,
            unique=True,
            db_index=True,
        )
        USERNAME_FIELD = 'email'

        class Meta:
            app_label = "testapp_tests"
