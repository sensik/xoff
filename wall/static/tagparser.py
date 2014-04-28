# tag parser for xoff

sampletext = 'kupa dupa #kaksoj kupsko gunwo #elo chuj #cipka #cipka gunwo #pipka'

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
	return tags