from urllib.request import urlopen
from bs4 import BeautifulSoup
from simhash import Simhash
import re
import pickle

class Webpage:
    def __init__(self):
        self.url = None
        self.title = None
        self.content = None
        self.outlinks = []

class Crawl:
    """ class crawl is a class dealing with crawling data from Website
        Args:
        url: root url for crawling
    """
    def __init__(self, url):
        self.frontier = [url]
        self.hash = set()
        self.fetchedurls = []
        self.simhash = Simhash()
        self.category_list = ['info', 'com', 'tech',
                              'sci', 'dev', 'pro', 'alg', 'learn', 'eng', 'math', 'oper', 'data']

    """ Description
    Args:
        in_dir: working directory
    """
    def crawl(self, in_dir, num=10):
        # url: string
        # title: string
        # content: string
        # outlinks: list
        i = 0
        while(len(self.fetchedurls)<num):
            # init new Webpage class
            webpage = Webpage()

            # fetch url and parse
            webpage.url = self.frontier.pop()  # 0: first element default: last element
            html = urlopen(webpage.url)
            bsObj = BeautifulSoup(html, "html.parser")  # get a bs object

            # check the category
            div = bsObj.find(name='div', id='mw-normal-catlinks')
            try:
                contents = div.find_all(name='a')
            except AttributeError:
                continue
            else:   
                tmp_category = ""
                for content in contents:
                    aText = content.get_text().lower()
                    tmp_category += aText
                # print(tmp_category)
                if(not any(category in tmp_category for category in self.category_list)):
                    continue
            
            # fetch title
            webpage.title = str(bsObj.title).replace(
                " - Wikipedia</title>", '').replace("<title>","")

            # fetch content
            tmp_content = ""
            div = bsObj.find(name='div', id='mw-content-text')
            ps = div.find_all(name='p')
            for p in ps:
                pText = p.get_text()
                tmp_content += pText
            webpage.content = tmp_content
            
            if (not webpage.title or not webpage.content):
                continue
            # content seen?
            tmp_hash = self.simhash.cal_simhash(tmp_content.split())
            """ content seen before

            """
            self.fetchedurls.append(webpage.url)

            # fetch outlinks
            tmp_outlinks = []
            newurls = div.find_all(
                'a', href=re.compile("^(/wiki/)((?!;)\S)*$"))
            for newurl in newurls:
                myurl = "https://en.wikipedia.org" + newurl.attrs['href']

                # dup URL elim
                if myurl not in self.fetchedurls and myurl not in self.frontier:
                    self.frontier.append(myurl)
                    tmp_outlinks.append(myurl)
            webpage.outlinks = tmp_outlinks

            # write to file
            with open(in_dir +'/'+ str(i), 'wb') as fwrite:
                pickle.dump(webpage, fwrite)

            i += 1
        fopen = open("fetchedurls","wb")
        pickle.dump(self.fetchedurls, fopen)


if __name__ == '__main__':
    url = "https://en.wikipedia.org/wiki/Computer_science"
    crawl = Crawl( url)
    crawl.crawl('./webpage', num=50)
    print(crawl.fetchedurls)
