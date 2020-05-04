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
        self.a = np.full([1, n], 1/n)

    """ build A matrix for multiple outlinks
    Args:
        doc_id: which doc to be processed for A matrix
        outlinks: all outlink this doc contains
    """
    def build_A_matrix(self, doc_id, outlinks):
        for j in range(len(outlinks)):
            try:
                num = self.fetchedurls.index(outlinks[j])
            except ValueError:
                continue
            else:
                self.A_matrix[doc_id][num] = 1

    """ refine the A matrix by using probability and teleport
    """
    def refine_A_matrix(self):
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

    def run(self, precision):
        # num = self.A_matrix.shape[0]
        # x = np.full([1, num],1/num)
        a_new = np.dot(self.a, self.A_matrix)
        print(a_new)
        error_sum = ((self.a - a_new)**2).sum()
        if (error_sum <= precision):
            return
        else:
            self.a = a_new
            self.run(precision)

if __name__ == '__main__':

    untitled = PageRank()
