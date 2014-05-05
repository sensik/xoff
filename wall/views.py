from django.shortcuts import render
from wall.models import Entry, Comment
from wall.forms import EntryForm, CommentForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login as auth_login
import datetime, re

def tagify(aText):
	aText = re.sub(r'#[a-zA-Z0-9]*', lambda m: m.group(0).lower(), aText)
	aText = re.sub(r'#(?P<tag>[a-zA-Z0-9]*)', '#<a href = "/tag/\g<tag>">\g<tag></a>', aText)
	return aText

def allEntries(request):
	entries = Entry.objects.all().order_by('-date')
	entry_pks = list(range(Entry.objects.all().order_by('-pk')[0].pk + 1))[1:] # wtf
	comments = Comment.objects.all()
	comments_by_entry_id = [Comment.objects.all().filter(entry_id = i) for i in entry_pks]
	
	for entry in entries:
		if len(comments_by_entry_id[entry.pk - 1]) > 0:
			entry.is_commented = True
		else:
			entry.is_commented = False
	
	for comment in comments:
		comment.entry_id = int(comment.entry_id)
	
	form = EntryForm(request.POST or None, initial = {'author': request.user.username})
	
	if request.POST:
		if form.is_valid():
			form.save()
		return HttpResponseRedirect('')
	
	for entry in entries:
		entry.content = tagify(entry.content)
	context = {'entries': entries, 'form': form, 'comments': comments, 'logged': request.user.is_authenticated(), 'username': request.user.username}
	return render(request, 'entries.html', context)

def detailEntry(request, pk):
	entry = Entry.objects.all().filter(pk = pk)[0]
	comments = Comment.objects.all().filter(entry_id = pk)
	for comment in comments:
		comment.content = tagify(comment.content)
	form = CommentForm(request.POST or None, initial = {'entry_id': pk, 'author': request.user.username}) # ugly - to be improved
	if request.POST:
		if form.is_valid():
			form.save()
		return HttpResponseRedirect('')
	entry.content = tagify(entry.content)
	context = {'entry': entry, 'comments': comments, 'form': form, 'logged': request.user.is_authenticated(), 'username': request.user.username}
	return render(request, 'entry.html', context)

def tag(request, tag):
	entries = Entry.objects.all().order_by('-date')
	tagentries = [entry for entry in entries if tag in entry.tags.split(', ')]
	for entry in tagentries:
		entry.content = tagify(entry.content)
	context = {'entries': tagentries, 'tag': tag, 'logged': request.user.is_authenticated(), 'username': request.user.username}
	return render(request, 'tag.html', context)
	
def tags(request):
	entries = Entry.objects.all()
	tags = [entry.tags for entry in entries if len(entry.tags) > 0]
	tags = ', '.join(tags).split(', ')
	context = {'tags': tags, 'logged': request.user.is_authenticated(), 'username': request.user.username}
	return render(request, 'tags.html', context)

def author(request, author):
	entries = Entry.objects.all().order_by('-date')
	authentries = [entry for entry in entries if entry.author == author]
	for entry in authentries:
		entry.content = tagify(entry.content)
	context = {'entries': authentries, 'author': author, 'logged': request.user.is_authenticated(), 'username': request.user.username}
	return render(request, 'author.html', context)
	
def signin(request):
	if request.user.is_authenticated():
		loggedmessage = 'You are already signed in, @' + request.user.username
		smallmessage = 'You can <a href = "/signout/">sign out</a> any time you want.'
	else:
		loggedmessage = 'sign in'
		smallmessage = ''
	if request.POST:
		username = request.POST.get('login')
		password = request.POST.get('password')
		user = authenticate(username = username, password = password)
		if user is not None:
			if user.is_active:
				auth_login(request, user)
				return HttpResponseRedirect('/../')
			else:
				context = {'loggedmessage': 'something went wrong :(', 'logged': request.user.is_authenticated(), 'username': request.user.username}
				return render(request, 'login.html', context)
		else:
			context = {'loggedmessage': 'something went wrong :(', 'logged': request.user.is_authenticated(), 'username': request.user.username}
			return render(request, 'login.html', context)
		#context = {'login': login, 'password': password}
	else:
		context = {'loggedmessage': loggedmessage, 'logged': request.user.is_authenticated(), 'username': request.user.username, 'smallmessage': smallmessage}
	return render(request, 'login.html', context)

def signout(request):
	logout(request)
	return HttpResponseRedirect('/../')

def post(request):
	if request.POST:
		dupa = request.POST
		context = {'dupa': dupa.get('dupa')}
	else:
		context = {'dupa': 0}
	return render(request, 'post.html', context)
	
'''def logintag(request): # doesn't work properly, to be fixed
	if request.user.is_authenticated():
		username = request.user.username
	else:
		username = None
	context = {'username': username, 'logged': request.user.is_authenticated()}
	return render(request, 'logintag.html', context)'''