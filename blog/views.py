from django.shortcuts import render, get_object_or_404 ,redirect
from django.http import HttpResponseRedirect
from .models import Profile, Tag, Article , Comment
from .forms import CommentForm

# Django Q objects use to create complex queries
# https://docs.djangoproject.com/en/3.2/topics/db/queries/#complex-lookups-with-q-objects
from django.db.models import Q


def home(request):

    # feature articles on the home page
    featured = Article.articlemanager.filter(featured=True)[0:3]

    context = {
        'articles': featured
    }

    return render(request, 'index.html', context)


def articles(request):

    # get query from request
    query = request.GET.get('query')
    # print(query)
    # Set query to '' if None
    if query == None:
        query = ''

    # articles = Article.articlemanager.all()
    # search for query in headline, sub headline, body
    articles = Article.articlemanager.filter(
        Q(headline__icontains=query) |
        Q(sub_headline__icontains=query) |
        Q(body__icontains=query)
    )

    tags = Tag.objects.all()

    context = {
        'articles': articles,
        'tags': tags,
    }

    return render(request, 'articles.html', context)


def article(request, article):

    article = get_object_or_404(Article, slug=article, status='published')

    context = {
        'article': article
    }

    return render(request, 'article.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Article, Comment
from .forms import CommentForm

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = article
            new_comment.save()
    else:
        comment_form = CommentForm()

    comments = article.comments.all()

    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'blog/article_detail.html', context)

# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment
from .forms import CommentForm

def add_comment(request, slug):
    # Get the article based on slug
    article = get_object_or_404(Article, slug=slug)

    if request.method == 'POST':
        # If the form was submitted, create a new comment instance
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = article
            comment.save()
            return redirect('blog:article', slug=article.slug)
    else:
        # If the form wasn't submitted, display a blank form
        form = CommentForm()

    # Render the template with the article and form context variables
    return render(request, 'blog/article.html', {'article': article, 'form': form})
