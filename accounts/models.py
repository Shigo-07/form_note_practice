from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.python_student = True
        user.save(using=self._db)
        return
    def create_customuser(self, email, password, staff=False, python_student=False, admin=False):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = staff
        user.python_student = python_student
        user.admin = admin
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.python_student = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Eメールアドレス",
        max_length=255,
        unique=True
    )
    username = models.CharField(
        "ユーザー名",
        max_length=150,
        default="名無しさん"
    )
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    python_student = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.admin

    def has_module_perms(self, app_label):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_python_student(self):
        return self.python_student

    @property
    def is_active(self):
        return self.active
