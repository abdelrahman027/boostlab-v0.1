from math import log
from urllib import request
from webbrowser import get
from django import http
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.template import context
from django.core.paginator import Paginator

from boostlab_posts.forms import CommentCreateForm, PostCreateForm, PostEditForm, ReplyCreateForm
from .models import Comment, Post, Reply, Tag

# Create your views here.
def home_view(request,tag=None):
    # if not request.user.is_authenticated:
    #     return redirect('account_login')
    if tag:
        posts= Post.objects.filter(tags__slug=tag)
        tag=get_object_or_404(Tag, slug=tag)
    else:
        posts= Post.objects.all()
    # categories= Tag.objects.all()
    paginator = Paginator(posts, 3)
    page = int(request.GET.get('page',1))
    try:
        posts = paginator.page(page)
    except:
        return HttpResponse("")
    context= {
        'posts': posts,
        # 'categories': categories,
        "tag": tag,
        'page': page
    }
    if request.htmx:
        return render(request, 'snippets/loop_home_posts.html', context=context)
    return render(request, 'boostlab_posts/home.html', context=context)



@login_required
def post_create_view(request):
    form = PostCreateForm()
    if request.method == 'POST':
        form = PostCreateForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
            # form.save_m2m()
            return redirect('home')
    context={'form': form}
    return render(request, 'boostlab_posts/post_create.html', context=context)

@login_required
def post_delete_view(request,pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully')
        return redirect('home')
    context = {
        'post': post
    }

    return render(request, 'boostlab_posts/post_delete.html', context=context)

@login_required
def post_edit_view(request,pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    form =PostEditForm(instance=post)
    if request.method == 'POST':
        form = PostEditForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully')
            return redirect('home')
    context = {
        'post': post,
        'form': form
    }

    return render(request, 'boostlab_posts/post_edit.html', context=context)


def post_page_view(request,pk):
    post = get_object_or_404(Post, id=pk)
    commentform =CommentCreateForm()
    replyform=ReplyCreateForm()

    
    if request.htmx:
        if 'top' in request.GET:
            # comments=post.comments.order_by('-likes')
            # comments=post.comments.filter(likes__isnull=False).order_by('-likes').distinct() #distinct() to remove duplicates
            comments=post.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
        else:
            comments=post.comments.all()
        return render(request,'snippets/loop_postpage_comments.html',{'comments':comments,'replyform':replyform})   
    
    context = {
        'post': post,
        'commentform': commentform,
        'replyform': replyform,
    }
    return render(request, 'boostlab_posts/post_page.html', context=context)


@login_required 
def comment_sent(request, pk):
    post = get_object_or_404(Post, id=pk)
    replyform = ReplyCreateForm()
    
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post            
            comment.save()
            
    context = {
        'post' : post,
        'comment': comment,
        'replyform': replyform
    }

    return render(request, 'snippets/add_comment.html', context)



@login_required
def comment_delete_view(request,pk):
    comment = get_object_or_404(Comment, id=pk, author=request.user)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully')
        return redirect('post' , comment.parent_post.id)
    context = {
        'comment': comment
    }

    return render(request, 'boostlab_posts/comment_delete.html', context=context)



@login_required 
def reply_sent(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    replyform=ReplyCreateForm() 
    # replyform = ReplyCreateForm()
    
    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment            
            reply.save()
    
    context = {
        'comment' : comment,
        'reply': reply,
        'replyform': replyform
    }
    return render(request, 'snippets/add_reply.html', context=context)


@login_required
def reply_delete_view(request,pk):
    reply = get_object_or_404(Reply, id=pk, author=request.user)
    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Reply deleted successfully')
        return redirect('post' , reply.parent_comment.parent_post.id)
    context = {
        'reply': reply
    }

    return render(request, 'boostlab_posts/reply_delete.html', context=context)


def like_toggle(model):
    def inner_func(func):
        def wrapper(request, *args, **kwargs):
            instance = get_object_or_404(model, id=kwargs['pk'])
            user_exists = instance.likes.filter(id=request.user.id).exists()
            if instance.author != request.user:
                if user_exists:
                    instance.likes.remove(request.user)
                else:
                    instance.likes.add(request.user)
            return func(request, instance)
        return wrapper
    return inner_func

@login_required
@like_toggle(Post)
def like_post(request,post):
    return render(request,'snippets/likes.html',{'post':post})

@login_required
@like_toggle(Comment)
def like_comment(request,comment):
    return render(request,'snippets/likes_comment.html',{'comment':comment})

@login_required
@like_toggle(Reply)
def like_reply(request,reply):
    return render(request,'snippets/likes_reply.html',{'reply':reply})