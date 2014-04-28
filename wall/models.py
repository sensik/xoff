from django.db import models
from django.template.defaultfilters import slugify
import datetime

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
			return ', '.join(tags)
		self.tags = parsetags(self.content)
		self.slug = slugify(self.content[:35])
		self.author = 'xxxx'
		self.date = datetime.datetime.now()
		super(Entry, self).save()