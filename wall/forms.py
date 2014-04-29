from django.forms import ModelForm
from wall.models import Entry, Comment

class EntryForm(ModelForm):
	class Meta:
		model = Entry
		fields = ['content']
		labels = {'content' : ''}
		
class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['content', 'entry_id']
		labels = {'content' : '', 'entry_id' : ''}