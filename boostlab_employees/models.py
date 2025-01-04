
from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static   
# Create your models here.
class Employee(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='profile_pics',null=True,blank=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    email=models.EmailField(max_length=100,null=True,blank=True)
    phone=models.CharField(max_length=100,null=True,blank=True)
    location=models.CharField(max_length=100,null=True,blank=True)
    address=models.TextField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar  = static('images/avatar_default.svg')
        return avatar
    
    @property
    def real_name(self):
        try:
            real_name = self.name
        except:
            real_name = self.user.username
        return real_name