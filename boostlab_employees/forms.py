from . models import *
from django import forms


class profileForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['user','department']
        widgets = {
            'image': forms.FileInput(),
            'bio': forms.Textarea(attrs={"rows": 3}),
            'address': forms.Textarea(attrs={"rows": 3}),
            
        }