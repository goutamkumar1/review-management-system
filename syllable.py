def syllables(word):
	count = 0
	vowels = 'aeiouy'
	word = word.lower().strip(".:;?!")
	if word[0] in vowels:
		count=count+1
	for index in range(1,len(word)):
		if word[index] in vowels and word[index-1] not in vowels:
			count +=1
	if word.endswith('e'):
		count -= 1
	if word.endswith('le'):
		count+=1
	if count == 0:
		count +=1
	return count

print(syllables("arithmetic"))