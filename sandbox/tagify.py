import re

def tagify(aText):
	aText = re.sub(r'#(?P<tag>[a-zA-Z0-9]*)', '<a href = "http://localhost:8000/tag/\g<tag>>\g<tag></a>"', aText)
	return aText.lower()