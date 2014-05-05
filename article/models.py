from django.db import models
from django.template.defaultfilters import slugify
import datetime

class Article(models.Model):
	slug = models.CharField(max_length = 50, editable = False)
	content = models.TextField()
	date = models.DateTimeField(editable = False)
	title = models.CharField(max_length = 100)
	
	def __str__(self):
		return self.title
		
	def save(self, *args, **kwargs):
		self.slug = slugify(self.title[:35])
		self.date = datetime.datetime.now()
		super(Article, self).save()