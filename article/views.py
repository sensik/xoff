from django.shortcuts import render
from article.models import Article

def article(request, slug):
	article = Article.objects.all().get(slug = slug)
	context = {'article': article, 'logged': request.user.is_authenticated(), 'username': request.user.username}
	return render(request, 'article.html', context)