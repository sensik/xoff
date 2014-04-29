from django.shortcuts import render
from wall.models import Entry
from wall.forms import EntryForm
from django.http import HttpResponseRedirect
import datetime, re

def tagify(aText):
	aText = re.sub(r'#[a-zA-Z0-9]*', lambda m: m.group(0).lower(), aText)
	aText = re.sub(r'#(?P<tag>[a-zA-Z0-9]*)', '#<a href = "/tag/\g<tag>">\g<tag></a>', aText)
	return aText

'''def parsetags(aText):
	tags = []
	for tag in range(aText.count('#')):
		aText = aText.split('#', 1)[1]
		try:
			if aText[0] != '#':
				tags.append(aText.split(' ')[0])
		except IndexError:
			return []
		while '' in tags:
			del tags[tags.index('')]
	return tags'''

def allEntries(request):
	entries = Entry.objects.all().order_by('-date')
	form = EntryForm(request.POST or None)
	if request.POST:
		if form.is_valid():
			form.save()
		return HttpResponseRedirect('')
	for entry in entries:
		entry.content = tagify(entry.content)
	context = {'entries' : entries, 'form' : form}
	return render(request, 'entries.html', context)

def detailEntry(request, pk):
	entry = Entry.objects.all().filter(pk = pk)[0]
	entry.content = tagify(entry.content)
	context = {'entry' : entry}
	return render(request, 'entry.html', context)

def tag(request, tag):
	entries = Entry.objects.all().order_by('-date')
	tagentries = [entry for entry in entries if tag in entry.tags.split(', ')]
	for entry in tagentries:
		entry.content = tagify(entry.content)
	context = {'entries' : tagentries, 'tag': tag}
	return render(request, 'tag.html', context)

def author(request, author):
	entries = Entry.objects.all().order_by('-date')
	authentries = [entry for entry in entries if entry.author == author]
	for entry in authentries:
		entry.content = tagify(entry.content)
	context = {'entries' : authentries, 'author': author}
	return render(request, 'author.html', context)