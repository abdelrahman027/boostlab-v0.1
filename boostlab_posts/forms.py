

from cProfile import label
from django import forms
from django.forms import ModelForm, widgets
from .models import Post,Comment, Reply


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['author','likes']
        labels= {
            "body": "Caption",
            "tags": "Category"
        }
        widgets = {
            "body": forms.Textarea(attrs={'rows':3,'placeholder':'Add a caption',"class": "text-4xl"}),
            "tags":forms.CheckboxSelectMultiple(),
        }
        
        
class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body','title','tags']
        labels= {
            "body": "Caption",
            "tags": "Category"
        }
        widgets = {
            "body": forms.Textarea(attrs={'rows':3,'placeholder':'Add a caption',"class": "text-4xl"}),
            "tags":forms.CheckboxSelectMultiple(),
        }



class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body' : forms.TextInput(attrs={'placeholder': 'Add comment ...'})
        }
        labels = {
            'body':''
        }
        
        
class ReplyCreateForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['body']
        widgets = {
            'body' : forms.TextInput(attrs={'placeholder': 'Add reply ...', 'class': "!text-sm"})
        }
        labels = {
            'body': ''
        }