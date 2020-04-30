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
        in_dir: working directory
        url: root url for crawling
    """
    def __init__(self, in_dir, url):
        self.frontier = [url]
        self.hash = set()
        self.fetchedurls = []
        self.simhash = Simhash()

    """ Description
    Args:
        arg: 
    Returns:
        return:
    """
    def crawl(self, num=10):
        # url: string
        # title: string
        # content: string
        # outlinks: list
        i = 0
        while(len(self.fetchedurls)<=num):
            # init new Webpage class
            webpage = Webpage()

            # fetch url and parse
            webpage.url = self.frontier.pop()
            html = urlopen(webpage.url)
            bsObj = BeautifulSoup(html, "html.parser")  # get a bs object

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
            fopen = open(str(i)+".txt", "wb")
            pickle.dump(webpage.url, fopen)
            pickle.dump(webpage.title, fopen)
            pickle.dump(webpage.content, fopen)
            pickle.dump(webpage.outlinks, fopen)

            # fopen.write(webpage.url)
            # fopen.write(webpage.title)
            # fopen.write(webpage.content)
            # fopen.write(" ".join(webpage.outlinks))
            i += 1
        fopen = open("fetchedurls.txt","wb")
        pickle.dump(self.fetchedurls, fopen)


if __name__ == '__main__':
    url = "https://en.wikipedia.org/wiki/Computer_science"
    crawl = Crawl('./webpage', url)
    crawl.crawl()
    print(crawl.fetchedurls)
