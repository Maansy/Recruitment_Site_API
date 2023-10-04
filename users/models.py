from django.db import models 
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
# Create your models here.

class CustomUserManager(UserManager):
    def _create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email,password,**extra_fields)
    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(email,password,**extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_manager = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_interviewer = models.BooleanField(default=False)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Users'
        ordering = ['email']

    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name or self.email.split('@')[0]