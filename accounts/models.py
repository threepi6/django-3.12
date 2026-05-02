from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager



#class CustomUserModel(AbstractUser):
#    id_code = models.CharField(max_length=10, blank=True)
#    phone = models.CharField(max_length=12, blank=True)


class CustomeManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            return ValueError("email can not be empty...!")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)
        #kwargs.setdefault("is_abbas", True)
        if kwargs.get("is_staff") is not True:
            raise ValueError("is_staff for superuser vajebeh")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("is_superuser for superuser vajebeh")
        if kwargs.get("is_active") is not True:
            raise ValueError("is_active for superuser vajebeh")
        #if kwargs.get("is_abbas") is not True:
            #raise ValueError("is_abbas for superuser vajebeh")
        return self.create_user(email, password, **kwargs)
        
class UserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    #id_code = models.CharField(max_length=10, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    #is_abbas = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    objects = CustomeManager()

    def __str__(self):
        return self.email


def validate_mobile(phone:str):
    if len(phone) != 11:
        raise ValueError ("phone must be 11 char")
    if not phone.isdigit():
        raise ValueError ("phone must be number")
    if not phone.startswith("09"):
        raise ValueError ("phone must start with 09")

def validate_idcode(id_code:str):
    if len(id_code) != 10:
        raise ValueError ("id_code must be 11 char")
    if not id_code.isdigit():
        raise ValueError("id_code must be number")


class UserProfile(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, null=True, blank=True, validators=[validate_mobile])
    id_code = models.CharField(max_length=10, null=True, blank=True, validators=[validate_idcode])
    image = models.ImageField(upload_to="profile/", null=True, blank=True)
