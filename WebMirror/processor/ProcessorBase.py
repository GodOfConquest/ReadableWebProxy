


import runStatus
runStatus.preloadDicts = False

# import Levenshtein as lv



import WebMirror.util.urlFuncs as urlFuncs
import urllib.parse
import LogBase
import TextScrape.gDocParse as gdp
import abc




class DownloadException(Exception):
	pass



########################################################################################################################
#
#	##     ##    ###    #### ##    ##     ######  ##          ###     ######   ######
#	###   ###   ## ##    ##  ###   ##    ##    ## ##         ## ##   ##    ## ##    ##
#	#### ####  ##   ##   ##  ####  ##    ##       ##        ##   ##  ##       ##
#	## ### ## ##     ##  ##  ## ## ##    ##       ##       ##     ##  ######   ######
#	##     ## #########  ##  ##  ####    ##       ##       #########       ##       ##
#	##     ## ##     ##  ##  ##   ###    ##    ## ##       ##     ## ##    ## ##    ##
#	##     ## ##     ## #### ##    ##     ######  ######## ##     ##  ######   ######
#
########################################################################################################################




GLOBAL_BAD = [
			'gprofiles.js',
			'netvibes.com',
			'accounts.google.com',
			'edit.yahoo.com',
			'add.my.yahoo.com',
			'public-api.wordpress.com',
			'r-login.wordpress.com',
			'twitter.com',
			'facebook.com',
			'public-api.wordpress.com',
			'wretch.cc',
			'ws-na.amazon-adsystem.com',
			'delicious.com',
			'paypal.com',
			'digg.com',
			'topwebfiction.com',
			'/page/page/',
			'addtoany.com',
			'stumbleupon.com',
			'delicious.com',
			'reddit.com',
			'newsgator.com',
			'technorati.com',
			'feeds.wordpress.com',
	]

GLOBAL_DECOMPOSE_BEFORE = [
			{'name'     : 'likes-master'},  # Bullshit sharing widgets
			{'id'       : 'jp-post-flair'},
			{'class'    : 'post-share-buttons'},
			{'class'    : 'commentlist'},  # Scrub out the comments so we don't try to fetch links from them
			{'class'    : 'comments'},
			{'id'       : 'comments'},
		]

GLOBAL_DECOMPOSE_AFTER = []

class PageProcessor(LogBase.LoggerMixin, metaclass=abc.ABCMeta):


	_relinkDomains  = []
	_scannedDomains = []
	_badwords       = []

	# Hook so plugins can modify the internal URLs as part of the relinking process
	def preprocessReaderUrl(self, inUrl):
		return inUrl


	def convertToReaderUrl(self, inUrl):
		inUrl = urlFuncs.urlClean(inUrl)
		inUrl = self.preprocessReaderUrl(inUrl)
		# The link will have been canonized at this point
		url = '/books/render?url=%s' % urllib.parse.quote(inUrl)
		return url

	def convertToReaderImage(self, inStr):
		inStr = urlFuncs.urlClean(inStr)
		return self.convertToReaderUrl(inStr)

	def relink(self, soup, imRelink=None):
		# The google doc reader relinking mechanisms requires overriding the
		# image relinking mechanism. As such, allow that to be overridden
		# if needed
		# print("relink call!")
		# print(self._relinkDomains)
		if not imRelink:
			imRelink = self.convertToReaderImage


		for (isImg, tag, attr) in urlFuncs.urlContainingTargets:

			if not isImg:
				for link in soup.findAll(tag):
					try:
						# print("Link!", self.checkRelinkDomain(link[attr]), link[attr])
						if self.checkRelinkDomain(link[attr]):
							link[attr] = self.convertToReaderUrl(link[attr])

						if "google.com" in urllib.parse.urlsplit(link[attr].lower()).netloc:
							link[attr] = gdp.trimGDocUrl(link[attr])
							# print("Relinked", link[attr])
					except KeyError:
						continue

			else:
				for link in soup.findAll(tag):
					try:
						link[attr] = imRelink(link[attr])

						if tag == 'img':
							# Force images that are oversize to fit the window.
							link["style"] = 'max-width: 95%;'

							if 'width' in link.attrs:
								del link.attrs['width']
							if 'height' in link.attrs:
								del link.attrs['height']

					except KeyError:
						continue

		return soup



	# check if domain `url` is a sub-domain of the domains we should relink.
	def checkRelinkDomain(self, url):
		# if "drive" in url:

		# print("CheckDomain", any([rootUrl in url.lower() for rootUrl in self._relinkDomains]), url)
		# print(self._relinkDomains)
		# dom = list(self._relinkDomains)
		# dom.sort()
		# for rootUrl in dom:
		# 	print(rootUrl in url.lower(), rootUrl)

		return any([rootUrl in url.lower() for rootUrl in self._relinkDomains])



	# check if domain `url` is a sub-domain of the scanned domains.
	def checkDomain(self, url):
		# if "drive" in url:
		for rootUrl in self._scannedDomains:
			if urllib.parse.urlsplit(url).netloc:
				if urllib.parse.urlsplit(url).netloc == rootUrl:
					return True

			if url.lower().startswith(rootUrl):
				return True

		# print("CheckDomain False", url)
		return False

	def checkFollowGoogleUrl(self, url):
		'''
		I don't want to scrape outside of the google doc document context.

		Therefore, if we have a URL that's on docs.google.com, and doesn't have
		'/document/d/ in the URL, block it.
		'''
		# Short circuit for non docs domains
		url = url.lower()
		netloc = urllib.parse.urlsplit(url).netloc
		if not "docs.google.com" in netloc:
			return True

		if '/document/d/' in url:
			return True

		return False


	def processLinkItem(self, url, baseUrl):
		url = gdp.clearOutboundProxy(url)
		url = gdp.clearBitLy(url)

		# Filter by domain
		if not self.checkDomain(url):
			# print("Filtering", self.checkDomain(url), url)
			return


		# and by blocked words
		for badword in self._badwords:
			if badword in url:
				# print("hadbad", self.checkDomain(url), url)

				return



		if not self.checkFollowGoogleUrl(url):
			return

		url = urlFuncs.urlClean(url)

		if "google.com" in urllib.parse.urlsplit(url.lower()).netloc:
			url = gdp.trimGDocUrl(url)

			if url.startswith('https://docs.google.com/document/d/images'):
				return

			# self.log.info("Resolved URL = '%s'", url)
			ret = self.processNewUrl(url, baseUrl)
			return ret
			# self.log.info("New G link: '%s'", url)

		else:
			# Remove any URL fragments causing multiple retreival of the same resource.
			if url != gdp.trimGDocUrl(url):
				print('Old URL: "%s"' % url)
				print('Trimmed: "%s"' % gdp.trimGDocUrl(url))
				raise ValueError("Wat? Url change? Url: '%s'" % url)
			ret = self.processNewUrl(url, baseUrl)
			# print("Returning:", ret)
			return ret
			# self.log.info("Newlink: '%s'", url)


	def extractLinks(self, soup, baseUrl):
		# All links have been resolved to fully-qualified paths at this point.
		ret = []
		for (dummy_isImg, tag, attr) in urlFuncs.urlContainingTargets:

			for link in soup.findAll(tag):

				# Skip empty anchor tags
				try:
					url = link[attr]
				except KeyError:
					continue


				item = self.processLinkItem(url, baseUrl)
				if item:
					ret.append(item)

		return ret


	def extractImages(self, soup, baseUrl):
		ret = []
		for imtag in soup.find_all("img"):
						# Skip empty anchor tags
			try:
				url = imtag["src"]
			except KeyError:
				continue

			item = self.processImageLink(url, baseUrl)
			if item:
				ret.append(item)
		return ret



	def postprocessBody(self, soup):
		return soup

	def preprocessBody(self, soup):
		return soup


	# Methods to allow the child-class to modify the content at various points.
	def extractTitle(self, srcSoup, doc, url):
		title = doc.title()
		if title:
			return title
		if srcSoup.title:
			return srcSoup.title.get_text().strip()


		return "'%s' has no title!" % url



	def processNewUrl(self, url, baseUrl=None, istext=True):
		if not url.lower().startswith("http"):
			if baseUrl:
				# If we have a base-url to extract the scheme from, we pull that out, concatenate
				# it onto the rest of the url segments, and then unsplit that back into a full URL
				scheme = urllib.parse.urlsplit(baseUrl.lower()).scheme
				rest = urllib.parse.urlsplit(baseUrl.lower())[1:]
				params = (scheme, ) + rest

				# self.log.info("Had to add scheme (%s) to URL: '%s'", scheme, url)
				url = urllib.parse.urlunsplit(params)

			elif self.ignoreBadLinks:
				self.log.error("Skipping a malformed URL!")
				self.log.error("Bad URL: '%s'", url)
				return
			else:
				raise ValueError("Url isn't a url: '%s'" % url)
		if gdp.isGdocUrl(url) or gdp.isGFileUrl(url):
			if gdp.trimGDocUrl(url) != url:
				raise ValueError("Invalid link crept through! Link: '%s'" % url)


		if not url.lower().startswith('http'):
			raise ValueError("Failure adding scheme to URL: '%s'" % url)

		if not self.checkDomain(url) and istext:
			raise ValueError("Invalid url somehow got through: '%s'" % url)

		if '/view/export?format=zip' in url:
			raise ValueError("Wat?")
		return url

