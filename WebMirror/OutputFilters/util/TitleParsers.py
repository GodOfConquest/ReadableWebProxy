
#!/usr/bin/python
# from profilehooks import profile
import urllib.parse
import re
import json
import logging
from WebMirror.OutputFilters import AmqpInterface
import settings
from WebMirror.util.titleParse import TitleParser


from WebMirror.OutputFilters.util.MessageConstructors import buildReleaseMessage

# pylint: disable=W0201


skip_filter = [
	"www.baka-tsuki.org",
	"re-monster.wikia.com",
]

def extractTitle(inStr):
	# print("Parsing: '%s'" % inStr)
	p    = TitleParser(inStr)
	vol  = p.getVolume()
	chp  = p.getChapter()
	frag = p.getFragment()
	post = p.getPostfix()
	return vol, chp, frag, post

def extractChapterVol(inStr):
	vol, chp, dummy_frag, dummy_post = extractTitle(inStr)
	return chp, vol

def extractVolChapterFragmentPostfix(inStr):
	vol, chp, frag, post = extractTitle(inStr)
	return vol, chp, frag, post

def extractChapterVolFragment(inStr):
	vol, chp, frag, dummy_post = extractTitle(inStr)
	return chp, vol, frag
