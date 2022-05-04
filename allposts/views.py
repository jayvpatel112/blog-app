from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post, Comment
from .forms import CommentForm

# Create your views here.

def index(request):
    latest_blog = Post.objects.all().order_by("-date")[:3]
    return render(request, "allposts/index.html", {"posts": latest_blog})

def posts(request):
    all_blog_post = Post.objects.all()
    return render(request, "allposts/index.html", {"posts": all_blog_post})

def is_stored_post(request, post_id):
    stored_post = request.session.get("stored_post")
    if stored_post is not None:
        return str(post_id) in stored_post
    else:
        return False

def post_detail(request, slug):
    single_post = Post.objects.get(slug=slug)
    form = CommentForm()
    comments = Comment.objects.filter(post=single_post)

    is_saved_for_later= is_stored_post(request, single_post.id)
    
    if request.method=="POST":
        single_post = Post.objects.get(slug=slug)
        form = CommentForm(request.POST)

        is_saved_for_later= is_stored_post(request, single_post.id)

        if form.is_valid():
            print(form.cleaned_data)
            comment = form.save(commit=False)
            comment.post = single_post
            comment.save()

            form = CommentForm()
            return HttpResponseRedirect(reverse("post-detail", args=[slug]))
        return render(request, "allposts/post_detail.html", {"post_detail": single_post, "form":form, "allcomments": comments, "is_saved_for_later":is_saved_for_later})
    
    return render(request, "allposts/post_detail.html", {"post_detail": single_post, "form":form, "allcomments": comments, "is_saved_for_later":is_saved_for_later})

def read_later(request):

    if request.method == "POST":
        stored_post = request.session.get("stored_post")

        if stored_post is None:
            stored_post = []
        
        post_id = request.POST["post_id"]

        if post_id not in stored_post:
            stored_post.append(post_id)
        else:
            stored_post.remove(post_id)
        request.session["stored_post"] = stored_post

        return HttpResponseRedirect("/read-later")
    
    #get method
    stored_post = request.session.get("stored_post")

    context = {}

    if stored_post is None or len(stored_post)==0:
        context["posts"] = []
        context["has_posts"] = False
    else:
        posts = Post.objects.filter(id__in=stored_post)
        context["posts"] = posts
        context["has_posts"] = True

    return render(request, "allposts/stored_post.html", context)