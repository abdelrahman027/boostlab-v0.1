

from cProfile import label
from django import forms
from django.forms import ModelForm, widgets
from .models import Activity, Task, File




class TaskCreateForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','due_date','assigned_to']
        labels= {
            "title": "Title",
            "description": "Description",
            "due_date": "Deadline",
            "assigned_to": "Employees",
        }
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
        

class TaskEditForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','due_date','assigned_to',"completed"]
        labels= {
            "title": "Title",
            "description": "Description",
            "due_date": "Deadline",
            "assigned_to": "Employees",
            "completed": "Completed"
        }
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class ActivityCreateForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['activity_file','description']
        labels= {
            "activity_file": "File",
            "description": "Description"
        }
        
        
class FileCreateForm(ModelForm):
    class Meta:
        model = File
        fields = ['file','description']   
        labels= {
            "file": "File",
            "description": "Description"
        }