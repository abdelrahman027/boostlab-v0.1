from math import log
from django.contrib.auth import login, logout
from django.db.models import Count
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from boostlab_posts.forms import ReplyCreateForm


from .forms import *


# Create your views here.
@login_required
def profile_view(request,username=None):
    if username:
        logged_employee = get_object_or_404(Employee, user__username=username)
    else:
        try:
            logged_employee = request.user.employee
        except:
            return redirect('account_login')
    posts = logged_employee.user.posts.all()
    
    if request.htmx:
        if 'top-posts' in request.GET:
            posts =logged_employee.user.posts.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
        elif 'top-comments' in request.GET:
            comments =logged_employee.user.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
            replyform = ReplyCreateForm()
            return render(request, 'snippets/loop_profile_comments.html', { 'comments': comments, 'replyform': replyform })
        elif 'liked-posts' in request.GET:
            posts =logged_employee.user.likedposts.order_by('-likedpost__created')
        return render(request,'snippets/loop_profile_posts.html',{'posts':posts})
    context = {
        'logged_employee': logged_employee,
        'posts': posts
    }
    return render(request, 'boostlab_employees/profile.html', context=context)

@login_required
def profile_edit_view(request):
    logged_employee = request.user.employee
    form = profileForm(instance=logged_employee)
    if request.method == 'POST':
        form = profileForm(request.POST,request.FILES, instance=logged_employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    if request.path == reverse('profile-onboarding'):
        template = 'boostlab_employees/profile_onboarding.html'
    else:
        template = 'boostlab_employees/profile_edit.html'
    context = {
        'logged_employee': logged_employee,
        'form': form
    }
    return render(request, template, context=context)

@login_required
def profile_delete_view(request):
    user=request.user
    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted successfully')
        return redirect('account_login')
    return render(request, 'boostlab_employees/profile_delete.html')