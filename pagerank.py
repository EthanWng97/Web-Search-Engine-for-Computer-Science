import numpy as np


class PageRank:
    """ class PageRank is a class dealing with pagerank function
        Args:
        dictionary_file: the name of the dictionary.
        postings_file: the name of the postings
    """
    def __init__(self, fetchedurls):
        self.fetchedurls = fetchedurls
        n = len(fetchedurls)
        self.A_matrix = np.zeros(shape=(n, n), dtype=np.float)

    """ Description
    Args:
        arg: 
    Returns:
        return:
    """
    def build_A_matrix(self, doc_id, outlinks):
        for j in range(len(outlinks)):
            try:
                num = self.fetchedurls.index(outlinks[j])
            except ValueError:
                continue
            else:
                self.A_matrix[doc_id][num] = 1

    """ Description
    Args:
        arg: 
    Returns:
        return:
    """
    def refine_A_matrix(self, doc_id, outlinks):
        num = self.A_matrix.shape[0]
        for i in range(self.A_matrix.shape[0]):

            # Markov chains
            if(np.sum(self.A_matrix[i])):
                self.A_matrix[i] /= np.sum(self.A_matrix[i])
            else:
                self.A_matrix[i] = 1/num
                continue

            # Teleport
            for j in range(self.A_matrix.shape[1]):
                self.A_matrix[i][j] = 0.1 * \
                    (1/num) + 0.9*self.A_matrix[i][j]

if __name__ == '__main__':

    untitled = PageRank()
