<h1 align="left">Web-Search-Engine-for-Computer-Science</h1>

## Full document
> [Medium](https://medium.com/navepnow/web-search-engine-for-computer-science-71ddae583f36)

## Prerequisites

* Python 3.7.6

## Install

    git clone https://github.com/NavePnow/Web-Search-Engine-for-Computer-Science.git

## Usage

### Crawling

    python3 crawling.py

**parameter setting**

    url = "https://en.wikipedia.org/wiki/Outline_of_computer_science"    
    crawl = Crawl(url, 'robots.txt')    
    crawl.get_rules()    
    crawl.crawl('./webpage', num=2000)

1. `url`: root link for crawling
2. `Crawl(url, ‘robots.txt’)`: robots.txt of wikipedia
3. `crawl.crawl('./webpage', num=2000)`: folder of saved webpages and number of crawling webpages
### Index

    python3 index.py -i directory-of-documents -d dictionary-file -p postings-file

1. Documents to be indexed are stored in `directory-of-documents`
2. `dictionary-file`: This file will store `array a`, `average length of total docs`, `info of docs` and `dictionary`.
3. `postings-file`: This file will store `tf`, `doc_id` and `position` of each term.


### Search

    python3 search.py -d dictionary-file -p postings-file -q query-file -o output-file-of-results

1. `dictionary-file`: This file is generated from index.py, which contains `array a`, `average length of total docs`, `info of docs` and dictionary.
2. `postings-file`: This file is generated from index.py, which contains `tf`, `doc_id` and `position` of each term.
3. `query-file`: This file contains several queries to be tested.
4. `output-file-of-results`: This file contains the result and corresponding urls from queries.txt

**Advanced option**

    -e  enable query expansion
    -f  disable relevance feedback
    -s  enable printing score

## Run tests
    python3 search.py -d dictionary.txt -p postings.txt -q queries.txt -o output.txt

## Author

👤 **Evan** — *Crawling, PageRank, Indexer, query expansion*

* Twitter: [@NavePnow](https://twitter.com/NavePnow)
* Github: [@NavePnow](https://github.com/NavePnow)

👤 **Rulin** — *Searcher, relevance feedback*
* Github: [@XJDKC](https://github.com/XJDKC)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!
Feel free to check [issues page](https://github.com/NavePnow/Web-Search-Engine-for-Computer-Science/issues).

## 💰 Show your support

Give a ⭐️ if this project helped you!

| PayPal                                                                                                                                                                       | Patron                                                                                                    |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| [![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=DSZJCN4ZUEW74&currency_code=USD&source=url) |   <a href="https://www.patreon.com/NavePnow"> <img src="https://c5.patreon.com/external/logo/become_a_patron_button@2x.png" width="160"> </a>

## 📖 Reference
* [*SimHash*](https://en.wikipedia.org/wiki/SimHash)
* [*WordNet*](https://en.wikipedia.org/wiki/WordNet)
* [*CS3245*](https://www.comp.nus.edu.sg/~cs3245/syllabus.html)
* [*CS3245-NUS-HW3*](https://github.com/cs-course-stu/CS3245-NUS-HW3)
* [*CS3245-NUS-HW4*](https://github.com/cs-course-stu/CS3245-NUS-HW4)