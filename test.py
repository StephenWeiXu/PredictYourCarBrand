
tweetText = "rt @weixu x80 ford car brand new price http://t.co/r26p8jlit7"

tweetText = tweetText.lower().split()

print tweetText

for ind in range(0, len(tweetText)):
	for word in tweetText:
		if '@' in word or 'http://' in word:
			tweetText.remove(word)
print tweetText

tweetText = ' '.join(tweetText)
print tweetText
