from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator

from model_utils import Choices

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Email adress required")
        if not username:
            raise ValueError("Username required")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class Account(AbstractUser):
    email               = models.EmailField(verbose_name='email',
        max_length=64, unique=True)
    username            = models.CharField(verbose_name='username',
        max_length=32, unique=True)
    display_name        = models.CharField(verbose_name='display_name',
        max_length=32, unique=True)
    weight              = models.IntegerField(verbose_name='weight', blank=True,
        validators=[MaxValueValidator(150), MinValueValidator(10)])
    boulder_grade       = models.IntegerField(choices=boulder_grades, blank=True)
    lead_grade          = models.IntegerField(choices=climbing_grades, blank=True)
    toprope_grade       = models.IntegerField(choices=climbing_grades, blank=True)


    is_admin            = models.BooleanField(default=False)
    is_staff            = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=True)

    boulder_grades = Choices('4', '4+', '5', '5+', '6a', '6a+', '6b', '6b+',
        '6c', '6c+', '7a', '7a+', '7b', '7b+', '7c', '7c+', '8a', '8a+', '8b',
        '8b+', '8c', '8c+', '9a')
    climbing_grades = Choices('I / 1', 'II / 2', 'II+ / 2+', 'III / 3',
        'IV / 4', 'V- / 4+', 'V / 5a', 'V+ / 5b', 'VI- / 5c', 'VI / 6a',
        'VI+ / 6a+', 'VII- / 6b', 'VII 6b+', 'VII+ / 6c', 'VIII- / 6c+',
        'VIII / 7a', 'VIII+ / 7a+', 'IX- / 7b',
        'IX / 7c', 'IX+ / 7c+', 'X- / 8a+', 'X / 8b', 'X+ / 8b+')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
