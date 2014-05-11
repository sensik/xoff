from django.shortcuts import render
from wall.models import Entry, Comment
from wall.forms import EntryForm, CommentForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login as auth_login
import datetime, re

def tagify(aText): # now it's overall markdown function
	# make all tags lowercase
	aText = re.sub(r'#[a-zA-Z0-9]*', lambda m: m.group(0).lower(), aText)
	
	# tags to urls
	aText = re.sub(r'#(?P<tag>[a-zA-Z0-9]*)', '#<a href = "/tag/\g<tag>">\g<tag></a>', aText)
	
	# nicks to urls
	aText = re.sub(r'@(?P<author>[a-zA-Z0-9]+)', '@<a href = "/author/\g<author>">\g<author></a>', aText)
	
	# problems
	#aText = re.sub(r'\[\[http://(?P<url>.+)\|(?P<title>.+)\]\]', '<a href = "http://\g<url>">\g<title></a>', aText)	# urls markdown - this works better
	#aText = re.sub(r'\[(?P<title>.+)\]\((?P<url>.+)\)', '<a href = "\g<url>">\g<title></a>', aText)			# urls markdown	- to be fixed
	#aText = re.sub(r'http://(?P<href>(.+/)+)(\n| )', '<a href = "\g<href>">http://\g<href></a>', aText)				# http:// to url
	
	# double asterisks to bold text
	aText = re.sub(r'\*\*(?P<text>(.+\n?)+)\*\*', '<b>\g<text></b>', aText)
	
	# double underscores to italics
	aText = re.sub(r'__(?P<text>(.+\n?)+)__', '<i>\g<text></i>', aText)
	
	# gravis to code
	aText = re.sub(r'`(?P<text>(.+\n?)+)`', '<code>\g<text></code>', aText)
	
	# > on newline to blockquote
	aText = re.sub(r'(^>|\n>)(?P<text>.+)', '<blockquote>\g<text></blockquote>', aText)
	
	# ! on newline to spoiler
	aText = re.sub(r'(^!|\n!)(?P<text>.+)', '<div class = "spoiler">\g<text></div>', aText)
	
	# newline to breakline
	aText = re.sub(r'\n', '<br>', aText)
	
	# 4 spaces to \t
	aText = re.sub(r'    ', '<pre>\t</pre>', aText)
	
	# raw url to hyperlink
	aText = re.sub(r'(?P<href>http://.+\.[a-z]{2,4})', '<a href = "\g<href>">\g<href></a>', aText)
	
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
	form = CommentForm(request.POST or None, initial = {'entry_id': pk, 'author': request.user.username, 'content': '@' + entry.author + ': '}) # ugly - to be improved
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
	else:
		context = {'loggedmessage': loggedmessage, 'logged': request.user.is_authenticated(), 'username': request.user.username, 'smallmessage': smallmessage}
	return render(request, 'login.html', context)

def signout(request):
	logout(request)
	return HttpResponseRedirect('/../')
	
def register(request):
	if request.user.is_authenticated():
		loggedmessage = 'You are already signed in, @' + request.user.username
	else:
		loggedmessage = 'sign up'
	context = {'loggedmessage': loggedmessage, 'logged': request.user.is_authenticated(), 'username': request.user.username}
	return render(request, 'register.html', context)