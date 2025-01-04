import profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from .models import Employee

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    user=instance
    if created:
        Employee.objects.create(user=user,email=user.email)
    else:
        employee=get_object_or_404(Employee,user=user)
        employee.email=user.email
        employee.save()
        
        
        
@receiver(post_save, sender=Employee)
def update_user(sender, instance, created, **kwargs):
    employee=instance
    if created == False:
        user= get_object_or_404(User, id=employee.user.id)
        if user.email!=employee.email:
            user.email=employee.email
            user.save()