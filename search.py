import re
import nltk
import sys
import getopt
from searcher import Searcher


# global variable
rate = 0.01
pivoted = False  # operate normalize according to the length of doc
expand = False   # operate query expansion
feedback = True  # operate relevance feedback
score = False    # print score of each result


def usage():
    print("usage: " +
          sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")
    print("options:\n"
          "  -d  dictionary file path\n"
          "  -p  postings file path\n"
          "  -q  queries file path\n"
          "  -o  search results file path\n"
          "  -e  enable query expansion\n"
          "  -f  disable relevance feedback\n"
          "  -s  enable printing score\n")


def run_search(dict_file, postings_file, queries_file, results_file, expand, feedback, rate, pivoted, score):
    """
    using the given dictionary file and postings file,
    perform searching on the given queries file and output the results to a file
    """
    print('running search on the queries...')
    # This is an empty method
    # Pls implement your code in below
    
    searcher = Searcher(dict_file, postings_file,
                        expand=expand, feedback=feedback, rate=rate, pivoted=pivoted, score=score)

    first_line = True
    with open(queries_file, 'r') as fin, \
            open(results_file, 'w') as fout:
        for line in fin:
            result, urls, score = searcher.search(line,[])
            result_urls = []
            for i in range(len(result)):
                result_urls.append(result[i])
                result_urls.append(urls[i])
            result_urls = map(str, result_urls)

            if first_line:
                result_urls = ' '.join(result_urls)
                first_line = False
            else:
                result_urls = '\n' + ' '.join(result_urls)

            fout.write(result_urls)

            if score:
                score = '\n' + ' '.join(map(str, score))
                fout.write(score)


dictionary_file = postings_file = file_of_queries = output_file_of_results = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:t:r:xns')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-d':
        dictionary_file = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    elif o == '-e':
        expand = True
    elif o == '-f':
        feedack = False
    elif o == '-s':
        score = True
    else:
        assert False, "unhandled option"

if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None:
    usage()
    sys.exit(2)

run_search(dictionary_file, postings_file, file_of_queries, file_of_output, expand,
           feedback, rate, pivoted, score)
