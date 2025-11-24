from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Article, Reply  # add Reply here
from .forms import ArticleForm, ReplyForm  # add ReplyForm

def article_list(request):
    articles = Article.objects.order_by('-created_at')
    return render(request, 'blog/article_list.html', {'articles': articles})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST' and request.user.is_authenticated:
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.article = article
            reply.author = request.user
            reply.save()
            return redirect('article_detail', pk=pk) 
    else:
        form = ReplyForm()

    replies = article.replies.order_by('created_at')
    return render(request, 'blog/article_detail.html', {
        'article': article,
        'replies': replies,
        'form': form
    })


@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_list')
    else:
        form = ArticleForm()

    return render(request, 'blog/article_form.html', {'form': form})

@login_required
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if article.author != request.user:
        return redirect('article_detail', pk=pk)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', pk=pk)
    else:
        form = ArticleForm(instance=article)

    return render(request, 'blog/article_form.html', {'form': form})

@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.author == request.user:
        article.delete()
    return redirect('article_list')
