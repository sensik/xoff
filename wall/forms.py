from django.forms import ModelForm
from wall.models import Entry

class EntryForm(ModelForm):
	class Meta:
		model = Entry
		fields = ['content']
		labels = {'content' : ''}