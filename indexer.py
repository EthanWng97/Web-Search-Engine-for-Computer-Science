import numpy as np
import os
import sys
import nltk
import pickle
import math
import time
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from collections import OrderedDict
from crawling import Webpage
from pagerank import PageRank

class Indexer:
    """ class Indexer is a class dealing with building index, saving it to file and loading it
        Args:
        dictionary_file: the name of the dictionary.
        postings_file: the name of the postings
    """

    def __init__(self, dictionary_file, postings_file):
        self.dictionary_file = dictionary_file
        self.postings_file = postings_file
        self.total_doc = {}
        self.dictionary = {}
        self.postings = {}

        self.file_handle = None
        self.average = 0
        self.normalize = True
        self.stem = PorterStemmer()
        self.rm_punct = RegexpTokenizer(r'\w+')
        self.stop_words = set(stopwords.words('english'))
        self.pagerank = None

    """ build index from documents stored in the input directory
    Args:
        in_dir: working path
        precision: value used for generating array a in pagerank
    """

    def build_index(self, in_dir, precision):
        print('indexing...')
        if (not os.path.exists(in_dir)):
            print("wrong file path!")
            sys.exit(2)
        files = os.listdir(in_dir)
        porter_stemmer = PorterStemmer()
        fopen = open(
            "/Users/wangyifan/Desktop/Web-Search-Engine-for-Computer-Science/fetchedurls", "rb")
        fetchedurls = pickle.load(fopen)
        # init PageRank class
        self.pagerank = PageRank(fetchedurls)
        # n = len(fetchedurls)
        # print(fetchedurls)
        # A_table = np.zeros(shape=(n,n),dtype=np.float)
        for i, file in enumerate(files):
            if not os.path.isdir(file):
                if (file == ".DS_Store"):
                    continue
                doc_id = int(file.replace(".txt", ""))
                doc_set = set()
                term_pos = 0
                self.total_doc[doc_id] = [0, 0]  # first element: length; second element: url
                # self.total_doc[doc_id] = 0

                webpage = Webpage()
                with open(in_dir + '/' + file,'rb') as f:
                    webpage = pickle.load(f)
                    
                    # process url
                    self.total_doc[doc_id][1] = webpage.url

                    # process outlinks
                    # contrust A table
                    self.pagerank.build_A_matrix(doc_id, webpage.outlinks)

                    # process title
                    term_pos, doc_set = self._process_corpus(
                        term_pos, doc_set, webpage.title, doc_id, title=True)
                    
                    # process content
                    term_pos, doc_set = self._process_corpus(
                        term_pos, doc_set, webpage.content, doc_id, title=False)

                # accumulate the length of doc
                if(self.normalize):
                    self.average += term_pos

                # calculate weight of each term
                length = 0
                for token in doc_set:
                    # convert raw tf into 1+log(tf)
                    self.postings[token][-1][1] = 1 + \
                        math.log(self.postings[token][-1][1], 10)

                    length += np.square(self.postings[token][-1][1])

                # assign length to each doc
                self.total_doc[doc_id][0] = np.sqrt(length)

                # normalize the 1+log(tf)
                for token in doc_set:
                    self.postings[token][-1][1] /= self.total_doc[doc_id][0]
        
        # calculate the average length of totoal doc
        if(self.normalize):
            self.average /= (i+1)

        # refine A Table
        self.pagerank.refine_A_matrix()
        # run pagerank algorithm
        self.pagerank.run(precision=precision)

    """ process title and content in each doc
    Args:
        term_pos: term position in the doc
        doc_set: set of words in the doc
        corpus: content or title
        doc_id: the id of the doc
        title: whether the corpus is title or not
    Returns:
        term_pos: processed term_pos
        doc_set: processed doc_set
    """

    def _process_corpus(self, term_pos, doc_set, corpus, doc_id, title=False):
        # tokenize
        if (title):
            tokens = self.rm_punct.tokenize(corpus)
        else:
            tokens = [word for sent in nltk.sent_tokenize(
                corpus) for word in nltk.word_tokenize(sent)]
        
        for token in tokens:
            # remove stopwords
            # if token.lower() in self.stop_words:
            #     continue

            # remove non alphanumeric
            if not token.isalnum():
                continue

            # stemmer.lower
            clean_token = self.stem.stem(token.lower())
            if (title):
                clean_token += ".title"
                # print(clean_token)
            if clean_token in self.dictionary:  # term exists
                if clean_token in doc_set:
                    self.postings[clean_token][-1][1] += 1

                    # insert position
                    self.postings[clean_token][-1][2].append(
                        term_pos)

                else:
                    doc_set.add(clean_token)

                    # insert position
                    self.postings[clean_token].append(
                        [doc_id, 1, [term_pos]])
            else:
                doc_set.add(clean_token)
                self.dictionary[clean_token] = 0

                # insert position
                self.postings[clean_token] = [
                    [doc_id, 1, [term_pos]]]  # {"term": [[1,2],[5,6]]}
            term_pos += 1
        return term_pos, doc_set

            
    """ save dictionary, postings and skip pointers given fom build_index() to file
    """

    def SavetoFile(self):
        print('saving to file...')

        dict_file = open(self.dictionary_file, 'wb+')
        post_file = open(self.postings_file, 'wb+')
        pos = 0

        # save postings to the file
        for key, value in self.postings.items():
            # save the offset of dictionary
            pos = post_file.tell()
            self.dictionary[key] = pos

            # print(self.postings[key])
            tmp = np.array(self.postings[key], dtype=object)

            # operate each postings
            for i in range(len(tmp)):
                # convert position list to the np.array
                tmp[i][2] = np.array(tmp[i][2])

            # sort the posting list according to he doc_id
            tmp = tmp[tmp[:, 0].argsort()]

            # split the total postings into doc, raw tf and position list
            doc = np.array(tmp[:, 0], dtype=np.int32)
            tf = np.array(tmp[:, 1], dtype=np.float32)

            # operate the position
            position = np.array(tmp[:, 2])

            # save all content to the file
            np.save(post_file, doc, allow_pickle=True)
            np.save(post_file, tf, allow_pickle=True)

            # save the position
            np.save(post_file, position, allow_pickle=True)
        
        # print(self.pagerank.a)
        # save array a generated from pagerank algorithm to the file
        pickle.dump(self.pagerank.a, dict_file)

        # save average length of doc to the file
        pickle.dump(self.average, dict_file)

        # save total_doc and dictionary
        pickle.dump(self.total_doc, dict_file)
        pickle.dump(self.dictionary, dict_file)

        print('save to file successfully!')
        return

    """ load dictionary from file
    Returns:
        a: array a generated from pagerank
        average: average of doc length
        total_doc: total doc_id
        dictionary: all word list
    """

    def LoadDict(self):
        print('loading dictionary...')
        with open(self.dictionary_file, 'rb') as f:
            a = pickle.load(f)
            self.average = pickle.load(f)
            self.total_doc = pickle.load(f)
            self.dictionary = pickle.load(f)

        print('load dictionary successfully!')
        return a, self.average, self.total_doc, self.dictionary

    """ load urls given list of doc_id
    Args:
        result: original list of doc_id from rank function
    Returns:
        tmp_url: list of urls corresponding to the doc_id
    """

    def LoadUrls(self, result):
        tmp_url = []
        for i in range(len(result)):
            tmp_url.append(self.total_doc[result[i]][1])
        
        return tmp_url

    """ load multiple postings lists from file
    Args:
        terms: the list of terms need to be loaded
    Returns:
        postings_lists: the postings lists correspond to the terms
    """

    def LoadTerms(self, terms):
        if not self.file_handle:
            self.file_handle = open(self.postings_file, 'rb')

        ret = {}
        for term in terms:
            if term in self.dictionary:
                self.file_handle.seek(self.dictionary[term])
                # load postings and position
                doc = np.load(self.file_handle, allow_pickle=True)
                log_tf = np.load(self.file_handle, allow_pickle=True)

                # load position
                position = np.load(self.file_handle, allow_pickle=True)

                # calculate idf
                df = len(doc)
                idf = math.log(len(self.total_doc) / df, 10)

                # return tuple
                ret[term] = (idf, doc, log_tf, position)

            else:
                idf = 0
                doc = np.empty(shape=(0, ), dtype=np.int32)
                log_tf = np.empty(shape=(0, ), dtype=np.float32)
                position = np.empty(shape=(0, ), dtype=object)
                ret[term] = (idf, doc, log_tf, position)

        return ret


if __name__ == '__main__':

    indexer = Indexer('dictionary.txt', 'postings.txt')
    start = time.time()
    indexer.build_index(
        '/Users/wangyifan/Desktop/Web-Search-Engine-for-Computer-Science/webpage', precision=0.00000001)
    indexer.SavetoFile()
    end = time.time()
    print('execution time: ' + str(end-start) + 's')
    # a, average, total_doc, dictionary = indexer.LoadDict()
    # print(total_doc)
    # terms = ['the']
    # print(indexer.LoadTerms(terms)['the'])
    # # print('./webpage' + '/' + str(indexer.LoadTerms(terms)['embark'][0][0]))
    # with open('./webpage' + '/' + '37', 'rb') as f:
    #     webpage = Webpage()
    #     webpage = pickle.load(f)
    #     print(webpage.content)
    #     print(webpage.url)
