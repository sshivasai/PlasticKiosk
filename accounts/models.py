from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from category.models import category
# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,user_role,password = None,
    phonenumber=None):
        if not email:
            raise ValueError('User must have a email address')
        if not username:
            raise ValueError('user must have a username')
        if not first_name:
            raise ValueError('user must have a First Name')
        if not last_name:
            raise ValueError('user must have a Last Name')
        if not user_role:
            raise ValueError('user must have a role')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            user_role = user_role,
            phonenumber = phonenumber
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
        
    def create_superuser(self,first_name,last_name,username,email,password, phonenumber = None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            user_role = "admin",
            password=password,
            phonenumber=phonenumber
        )
        user.is_retailer =True
        user.is_household = True
        user.is_superadmin = True
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save(using = self._db)
        return user


    
# Create your models here.
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100,unique=True)
    phonenumber = models.CharField(max_length=12)
    user_role = models.CharField(max_length=50)


    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    #for access control
    is_retailer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_household = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =  ['username','first_name','last_name','phonenumber']
    objects = MyAccountManager()
    def __str__(self):
        return self.first_name + " "+ self.last_name
    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,add_label):
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile',null=True, default='default/default-user.jpg')
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    user_role = models.ForeignKey(category,on_delete=models.CASCADE,blank=True,null=True)
    phone_number = models.CharField(max_length=12,blank=True,null=True)

    def __str__(self):
        return self.user.first_name

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'