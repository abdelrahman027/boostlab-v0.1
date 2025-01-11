
from django.db import models
from django.contrib.auth.models import User
from boostlab_employees.models import Manager

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    manager = models.ForeignKey(Manager, related_name='assigned_tasks', on_delete=models.SET_NULL, null=True,blank=True)
    assigned_to = models.ManyToManyField(User, related_name='tasks')
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Activity(models.Model):
    task = models.ForeignKey(Task, related_name='activities', on_delete=models.CASCADE)
    description = models.TextField()
    participant = models.ForeignKey(User, related_name='activities', on_delete=models.SET_NULL, null=True,blank=True)       
    activity_file = models.FileField(upload_to='activity_images',null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Activity for {self.task.title}: {self.description[:20]}"
    
    
class File(models.Model):
    task = models.ForeignKey(Task, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='task_files/')
    added_by = models.ForeignKey(User, related_name='added_files', on_delete=models.SET_NULL, null=True,blank=True)
    description = models.TextField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for {self.task.title}: {self.file.name}"
