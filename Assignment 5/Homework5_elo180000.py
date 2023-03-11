import re
import pickle
import requests
import urllib.request
from bs4 import BeautifulSoup
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from os import listdir
from os.path import isfile, join


STOPWORDS = set(stopwords.words('english'))


# Web Crawler Function
def crawler(first_URL):
    other_URLs = 0
    max_URLs = 16
    in_queue = [first_URL]
    web_crawler = []
    accept_keys = ['Candy', 'candy']
    # Loop to look through the queue to open and use any open/available URLs
    while other_URLs < max_URLs and in_queue:
        url = in_queue.pop(0)
        request = requests.get(url)
        URL_data = request.text
        soup = BeautifulSoup(URL_data, "html.parser")
        web_crawler.append(url)
        other_URLs += 1
        cnt = 0

        # Saves any links and uses filters
        for URL_link in soup.find_all('a'):
            URL_str = str(URL_link.get('href'))
            if any(URL_works in URL_str for URL_works in accept_keys):
                if '&' in URL_str:
                    j = URL_str.find('&')
                    URL_str = URL_str[:j]
                if URL_str.startswith('http'):
                    # Checks URL
                    if URL_str not in web_crawler and URL_str not in in_queue:
                        in_queue.append(URL_str)
                        cnt += 1
                        if cnt >= 5:
                            break
    return web_crawler


# Scrape function to take all text off each page
def Text_Scrape(queue):
    for url in queue:
        parser_html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(parser_html, "html.parser")
        # Using the URL, extract all text
        text = soup.get_text()
        # Pickle the scrape files and write in import_terms
        pickle.dump(text, open('sf/text{}.txt'.format(queue.index(url)), 'wb'))


def Scrape_Process():
    # Get list of pickle scrap files
    for file in [file for file in listdir('sf') if isfile(join('sf', file))]:
        # Open the scrape pickle file
        raw = pickle.load(open('sf/{}'.format(file), 'rb'))

        # Remove characters that isn't needed
        raw = raw.replace('\n', '').replace('\t', '').replace(u'\r', '')
        token_sent = sent_tokenize(raw)

        # Pickle the scrape text that has already been processed
        pickle.dump(token_sent, open('psf/{}'.format(file), 'wb'))


if __name__ == '__main__':
    # Topic is Candy
    url_list = crawler("https://en.wikipedia.org/wiki/Candy")
    Text_Scrape(url_list)
    Scrape_Process()

    # Extracting 25 important terms from each process file/URLs
    for file in [file for file in listdir('psf') if isfile(join('psf', file))]:
        token = []
        read_text = pickle.load(open('psf/{}'.format(file), 'rb'))
        regex = r'[^\w\s]'
        for rts in read_text:
            text = re.sub(regex, '', rts)
            token += word_tokenize(text)
        frequent_dict = FreqDist([words for words in token if not words.lower() in STOPWORDS])
        most_frequent_words = frequent_dict.most_common(25)

        print('Top 25 terms -', '{}:'.format(file), most_frequent_words)

        # Write as a pickle file
        pickle.dump(most_frequent_words, open('import_terms/{}'.format(file), 'wb'))

    top_10_terms = ['candy', 'sugar', 'candies', 'archived', 'made', 'chocolate', 'original', 'retrieved', 'children',
                    'food']
    Create_knowledge_base = {
        'M&Ms': 'Were first release in 1941, and since then have had an oversize impact on American popular culture',
        'Reeses_Peanut_Butter_Cup': '',
        'Kit_Kat': 'Kit Kat is the world first chocolate bar made from 100% sustainable cocoa',
        'Skittles': 'Skittles were first introduce in North America in 1979 as an import confectionery',
        'Star_Burst': 'Starburst was introduce in England in 1959.',
        'Snickers': 'Snickers were introduced in 1930.',
        'Sour_Patch_Kids': 'These deliciously chewy treats were originally named Mars Men to keep up with the space '
                           'craze during that time.',
        'Smarties': 'Smarties are colour-varied sugar-coated chocolate confectionery. They have been manufactured '
                    'since 1937',
        'Tootsie_Rolls': 'Tootsie Rolls Were WWII Energy Bars',
        'Gummy_Bears': 'Gummy Bears Were Originally Called “Dancing Bears.”'
    }
    pickle.dump(Create_knowledge_base, open('knowledge_base.p', 'wb'))
