from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, \
    BaseUserManager
from django_countries.fields import CountryField


# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, email, password, **other_fields):

        if not email:
            raise ValueError('Please provide a valid email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=150, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='user_avatars/', blank=True,
                               null=True)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    age = models.IntegerField(max_length=3)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Student(User):
    grade = models.IntegerField(max_length=2)
    school = models.CharField(max_length=150)
    homeroom_id = models.CharField(max_length=150)


class Teacher(User):
    school = models.CharField(max_length=150)


class homeroom_id(AbstractBaseUser, PermissionsMixin):
    homeroom_id = models.CharField(max_length=150)
    teacher_id = models.CharField(max_length=150)
