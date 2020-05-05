import numpy as np
import os
import sys
import nltk
import pickle
import math
import time
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
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

        self.average = 0
        self.normalize = True

    """ Description
    Args:
        arg: 
    Returns:
        return:
    """

    def build_index(self, in_dir):
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
        pagerank = PageRank(fetchedurls)
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
                self.total_doc[doc_id] = 0

                webpage = Webpage()
                with open(in_dir + '/' + file,'rb') as f:
                    webpage = pickle.load(f)
                    # if(doc_id == 0): 
                    #     print(webpage.url)
                    #     print(webpage.outlinks)
                    #     print(len(webpage.outlinks))
                    # contrust A table
                    pagerank.build_A_matrix(doc_id, webpage.outlinks)

                    # process content
                    # tokenize
                    tokens = [word for sent in nltk.sent_tokenize(
                        webpage.content) for word in nltk.word_tokenize(sent)]

                    for token in tokens:
                        # stemmer.lower
                        clean_token = porter_stemmer.stem(token.lower())

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

                # sqart the length and assign it to doc
                self.total_doc[doc_id] = np.sqrt(length)
        
        # calculate the average length of totoal doc
        if(self.normalize):
            self.average /= (i+1)

        # refine A Table
        pagerank.refine_A_matrix()

        # run pagerank algorithm
        pagerank.run(precision=0.001)
            



if __name__ == '__main__':

    index = Indexer('dictionary.txt', 'postings.txt')
    index.build_index(
        '/Users/wangyifan/Desktop/Web-Search-Engine-for-Computer-Science/webpage')
