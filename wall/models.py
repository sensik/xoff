from django.db import models
from django.template.defaultfilters import slugify
import datetime, re

class Entry(models.Model):
	slug = models.CharField(max_length = 50, editable = False)
	content = models.TextField()
	date = models.DateTimeField()
	author = models.CharField(max_length = 50)
	tags = models.TextField(editable = False)
	
	def __str__(self):
		return self.slug
		
	def save(self, *args, **kwargs):
		def parsetags(aText):
			alltags = re.findall(r'#(?P<tag>[a-zA-Z0-9]*)', aText)
			tags = [tag.lower() for tag in alltags]
			return ', '.join(tags)
		self.tags = parsetags(self.content)
		self.slug = slugify(self.content[:35])
		self.date = datetime.datetime.now()
		super(Entry, self).save()
		
class Comment(models.Model):
	slug = models.CharField(max_length = 50, editable = False)
	content = models.TextField()
	entry_id = models.CharField(max_length = 50)
	date = models.DateTimeField()
	author = models.CharField(max_length = 50)
	
	def __str__(self):
		return str(self.entry_id) + ' -- ' + self.slug
		
	def save(self, *args, **kwargs):
		self.slug = slugify(self.content[:35])
		self.date = datetime.datetime.now()
		super(Comment, self).save(*args, **kwargs)