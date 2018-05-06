import argparse
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
from collections import Counter

class linkParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for key, value in attrs:
                if key ==  'href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    self.links = self.links + [newUrl]

    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        if ("text/html" in response.getheader('Content-Type')):
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return htmlString, self.links
        else:
            print(response.getheader("Content-Type"))
            return "", []

def spider(url, word, maxPages):
    if "www." not in url:
        url = "www." + url

    if 'http://' not in url or "https://" not in url:
        print("No http protocol included in address, defaulting to https")
        url = "https://" + url

    pagesToVisit = [url]
    numberVisited = 0
    foundWord = False

    urlsFound = []
    totalCount = 0
    while numberVisited < maxPages and pagesToVisit != []:
        numberVisited += 1
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        try:
            print(numberVisited, "Visiting:", url)
            parser = linkParser()
            data, links = parser.getLinks(url)
            wordcount = Counter(data.split())
            pageWordCount = wordcount[word]
            if pageWordCount >-1:
                foundWord = True
                pagesToVisit = pagesToVisit + links
                urlsFound.append(url)
                print(str(pageWordCount) + " instances of word found at " + url)
                totalCount += pageWordCount
        except Exception as e:
            print(str(e))
    if foundWord:
        print(str(totalCount) + " instances of the word " +  word + " was found at " + ", ".join(urlsFound))
    else:
        if numberVisited >= maxPages:
            print("Ran out of pages")
        else:
            print("Word never found")

# Initiate parser for command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--address')
parser.add_argument('--word')
parser.add_argument('--upper')

args = vars(parser.parse_args())
print(args)

address = args['address']
word = args['word']
upper = int(args['upper'])
print("Starting spider at address", address, ", searching for key", word, "with page limit of", str(upper))
spider(address, word, upper)