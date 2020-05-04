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
        self.skip_pointer_list = []
        self.postings = {}

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

        # print(pagerank.A_matrix)
        # refine A Table
        pagerank.refine_A_matrix()
        # print(pagerank.x)

        # print(pagerank.A_matrix)

        # run pagerank algorithm
        pagerank.run(precision=0.001)
            
        # print(pagerank.A_matrix)


if __name__ == '__main__':

    index = Indexer('dictionary.txt', 'postings.txt')
    index.build_index(
        '/Users/wangyifan/Desktop/Web-Search-Engine-for-Computer-Science/webpage')
