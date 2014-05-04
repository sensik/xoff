from django.forms import ModelForm
from wall.models import Entry, Comment

class EntryForm(ModelForm):
	class Meta:
		model = Entry
		fields = ['content', 'author']
		labels = {'content' : '', 'author': ''}
		
class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['content', 'entry_id', 'author']
		labels = {'content' : '', 'entry_id' : '', 'author': ''}