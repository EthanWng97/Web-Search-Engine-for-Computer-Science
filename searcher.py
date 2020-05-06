import sys
import math
import nltk
import array
import heapq
import numpy as np
from indexer import Indexer
from refiner import Refiner
from refiner import QueryInfo
from nltk.corpus import stopwords
from collections import defaultdict
from nltk.stem.porter import PorterStemmer


class Searcher:
    """ Searcher is a class dealing with real-time querying.
        It implements the ranked retrieval based on the VSM(Vector Space Model).
        It also support Phrasal Queries and Pivoted Normalized Document Length.
    Args:
        dictionary_file: the file path of the dictionary
        postings_file: the file path of the postings
        rate: the penalty rate of the pivoted normalized document length
        expand: boolean indicator for using Query Expansion
        feedback: boolean indicator for using Relevance Feedback
        pivoted: boolean indicator for using pivoted normalized document length
    """

    def __init__(self, dictionary_file, postings_file, rate=0.01,
                 expand=True, feedback=True, pivoted=False, score=False):
        self.dictionary_file = dictionary_file
        self.postings_file = postings_file
        self.rate = rate
        self.pivoted = pivoted
        self.score = score

        self.stemmer = PorterStemmer()
        self.indexer = Indexer(dictionary_file, postings_file)
        self.refiner = Refiner(indexer=self.indexer,
                               expand=expand, feedback=feedback)

        self.indexer.LoadDict()

    """ Search and return docIds according to the boolean expression.
    Args:
        query: the query string
    Returns:
        result: the list of K most relevant docIds in response to the query
    """

    def search(self, query, relevant_docs):
        # step 1: let refiner to refine the query and get query_infos
        query_infos, postings_lists = self.refiner.refine(query, relevant_docs)

        # step 2: get candidate docs that need to rank(phrasal query)
        # step 2-1: get all the docs that contains all the terms in the query
        self._get_intersection(query_infos, postings_lists)

        # step 2-2: judging every doc whether it contains the phrase
        self._judge(query_infos, postings_lists)

        # step 3: rank documents get the result
        result, score = self.rank(query_infos, postings_lists)

        # step 4: return the result
        return result, score

    """ Rank the documents and return the K most relevant docIds.
        The result should be in the order of relevant.
    Args:
        query_infos: a list of instances of QueryInfo that contains the query
        postings_lists: the dictionary with terms to posting lists mapping
    Returns:
       result: the list of K most relevant docIds in response to the query
       score: the list of the scores corresponding to the docIds
    """

    def rank(self, query_infos, postings_lists):
        total_scores = defaultdict(lambda: 1)

        for query_info in query_infos:
            # step 1: Initialize variables
            terms = query_info.terms
            scores = defaultdict(lambda: 0)
            query_vector = query_info.query_vector

            # step 2: processing every document and every term
            for i, term in enumerate(terms):
                candidates = query_info.candidates
                postings_list = postings_lists[term]
                postings = postings_list[1]
                weights = postings_list[2]

                for j in range(0, len(postings)):
                    doc = postings[j]

                    if query_info.is_phrase and (doc not in candidates):
                        continue

                    weight = weights[j]
                    scores[doc] += weight * query_vector[i]

            # step 3: use pivoted document length
            """
            for doc in scores:
                length = self.total_doc[doc]
                if self.pivoted:
                    piv = 1 - self.rate + self.rate * length / self.average
                    scores[doc] /= length * piv
                else:
                    scores[doc] /= length
            """

            # step 4: update total scores
            for doc in scores:
                total_scores[doc] += scores[doc]

        # step 4: get the topK docs from the heap
        heap = [(total_scores[doc], -doc) for doc in total_scores]
        heap = heapq.nlargest(len(total_scores), heap, key=lambda x: x)

        result = [-item[1] for item in heap]

        score = []
        if self.score:
            score = [item[0] for item in heap]

        # step 5: return the topK docs
        return result, score

    """ Get the intersection of docs
    Args:
        query_infos: a list of instances of QueryInfo that contains the query
        postings_lists: the dictionary with terms to posting lists mapping
    """

    def _get_intersection(self, query_infos, postings_lists):
        for query_info in query_infos:
            terms = query_info.terms

            if not query_info.is_phrase:
                continue

            if len(terms) == 0:
               query_info.candidates = []
               continue

            # optimize the order of the merge
            costs = []
            for term in terms:
                postings = postings_lists[term][1]
                costs.append((term, len(postings)))

            costs.sort(key=lambda key: key[1])

            # perform pairwise merge
            result = postings_lists[costs[0][0]][1]
            for i in range(1, len(costs)):
                term = costs[i][0]
                postings = postings_lists[term][1]

                p1 = p2 = 0
                len1, len2 = len(result), len(postings)
                temp = array.array('i')

                while p1 < len1 and p2 < len2:
                    doc1 = result[p1]
                    doc2 = postings[p2]

                    if doc1 == doc2:
                        temp.append(doc1)
                        p1, p2 = p1 + 1, p2 + 1
                    elif doc1 < doc2:
                        p1 += 1
                    else:
                        p2 += 1

                result = temp

            # update the candidates
            query_info.candidates = set(result)

    """ Judging whether candidate documents contain the phrase
    Args:
        query_infos: a list of instances of QueryInfo that contains the query
        postings_lists: the dictionary with terms to posting lists mapping
    """

    def _judge(self, query_infos, postings_lists):
        for query_info in query_infos:
            tokens = query_info.tokens

            if not query_info.is_phrase:
                continue

            if len(tokens) <= 1:
                continue

            positions = defaultdict(lambda: [])
            candidates = query_info.candidates

            # get postions for docs
            for i, token in enumerate(tokens):
                postings_list = postings_lists[token]
                postings = postings_list[1]
                length = len(postings)
                for j in range(0, length):
                    docId = postings[j]
                    if docId in candidates:
                        positions[docId].append(postings_list[3][j])

            # judging every doc
            ans = set()
            for doc in positions:
                position = positions[doc]
                pointers = [0] * len(position)

                index = 1
                flag = False
                prev_pos = position[0][0]
                while True:
                    pointer = pointers[index]
                    length = len(position[index])

                    while pointer + 1 < length:
                        tmp = position[index][pointer + 1]
                        if tmp <= prev_pos + 1:
                            pointer += 1
                        else:
                            break

                    pointers[index] = pointer
                    cur_pos = position[index][pointer]

                    if cur_pos != prev_pos + 1:
                        index -= 1
                        pointers[index] += 1
                        if pointers[index] >= len(position[index]):
                            break
                        if index == 0:
                            index += 1

                        pointer = pointers[index - 1]
                        prev_pos = position[index - 1][pointer]
                        continue
                    else:
                        prev_pos = cur_pos
                        index += 1
                        if index >= len(position):
                            flag = True
                            break

                if flag:
                    ans.add(doc)

                query_info.candidates = ans


if __name__ == '__main__':
    # Create a Searcher
    searcher = Searcher('test-dictionary.txt', 'test-postings.txt', score=True)

    test_cases = [
        {"query": '"Computer Science" AND Refiner can tokenize query strings into terms and tokens',
         "relevant_docs": [0, 5]},
        {"query": '"Computer Science" AND Refiner can tokenize query strings into terms and tokens',
         "relevant_docs": [0]},
        {"query": '"Computer Science" AND Refiner can tokenize query strings into terms and tokens',
         "relevant_docs": [5]},
        {"query": '"Computer Science" AND Refiner can tokenize query strings into terms and tokens',
         "relevant_docs": []},
        {"query": '"Computer Science"',
         "relevant_docs": []}
    ]

    for i, test_case in enumerate(test_cases):
        query = test_case['query']
        relevant_docs = test_case['relevant_docs']
        result, score = searcher.search(query, relevant_docs)
        print("test case [%d]" % i)
        print("query:", query)
        print("relevant_docs", relevant_docs)
        print("result", result)
        print("score", score)
        print("")
