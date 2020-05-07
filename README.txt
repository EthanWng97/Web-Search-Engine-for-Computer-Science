This is the README file for A0213835H-A0214251W-A0168291X-A0168954L's submission.

== Python Version ==

We're using Python Version 3.7.6 for this assignment.

== General Notes about this assignment ==

We divide the whole program into two parts, the index part and the search part. The former is to build the inverted index,
calculate and record the normalised weighted tfs corresponding to the postings and save the index into file. The indexer will
also save the term positions in the doc to aid with handling phrasal queries. The searcher loads the inverted index, parse
the query, search for all relevant documents in response to the query.

We adopt the object-oriented programming approach to build the whole project, which greatly reduces the coupling between two parts.

[Indexer]
As for the index part, there are two main functions to solve the problem.
    1. Build index
        1.1 Process and store the fields we identified (court and date)
            1.1.1 Dictionaries are built for these fields, mapping the field content to the doc id
        1.2 Pre-process and store information about the zones (title and content)
            1.2.1 Remove all punctuations from title and content
            1.2.2 Stem the words and change all characters to lower case
            1.2.3 Append ".title" to words found in the title
            1.2.4 Add words to posting and store the doc id
            1.2.5 Store the position of each word in each document
	    1.3 Process the term frequencies of each document
	        1.3.1 Normalise and weight the term frequencies
	        1.3.2 Store resulting values in postings corresponding to each term and document
	    1.4 Calculate average length of each document
	        1.4.1 Divide the sum of all lengths of documents by the number of documents
	    1.5 Process postings to increase efficiency when retrieving information later on
	        1.5.1 Convert lists to numpy arrays
	        1.5.2 Sort the numpy arrays

    2. Save to file
	    2.1 For each term, save offset in the dictionary
	    2.2 Dump posting list for term into postings.txt
	    2.3 Dump calculated average in dictionary.txt
	    2.4 Dump mapping of doc ids to document length in dictionary.txt
	    2.5 Dump mapping of court field to doc id in dictionary.txt
	    2.6 Dump mapping of date field to doc id in dictionary.txt
	    2.7 Dump mapping of terms to offset in dictionary.txt

[Searcher] TODO: This is from hw3, needs to be edited for hw4
As for the search part, we use the following steps to process a request.
    1. Tokenize the query into tokens, the program will also count the number of each term
       in the query.
    2. Load postings lists for the terms in the expression from the postings.txt file.
       For terms that appear multiple times in the query, we just load once to reduce memory cost.
       The postings lists include the docids, tfs and positions if the phrase query is turned on.
    3. Get the docs that need to rank.
       This step is mainly used to filter documents when phrase query is turned on.
       [phrasal query filtering]
       3.1 Get all the docs that contains all the terms inthe query.
           Calculate the union of all postings lists, the searcher will merge them
           according to the size of the list.
       3.2 Judging every doc whether it contains the phrase.
           After step 3.1, the candidate docs contain all terms but they may not adjacent.
           So we need to ensure the candidate docs contain the phrase.
    4. Rank the candidate docs and get the result.
       4.1 Construct the query vector
           Based on the postings lists of terms, we can get the query vector.
       4.2 Processing every document and every term.
           To get the cosine value of document vector and the query vector as doc's score.
       4.3 Divide the score with the document length
           If the pivoted normalized document length is turned on, the score will be devided by
           the pivoted normalized document length.
       4.4 Use max-head heap to get the K(can be set by user) most relevant docIds.
           If printing score is enabled, the scores will be returned too.
    5. Return the results

== Files included with this submission ==

* index.py: The file in this assignment using Indexer to build the index and dump to file.
* indexer.py: The file contains the Indexer class which helps to build, load and dump the inverted index.
* search.py: The file in this assignment using Seacher to get all relevant documents.
* searcher.py: The file contains the Searcher class which helps to search the most relevant documents of the query.
* README.txt: This file contains an overview of this assignment and the algorithm's we used to solve it.
TODO: remove Essay.txt if we are not doing it (probably not right)
* ESSAY.txt: This file contains essay questions mentioned on HW#3
* dictionary.txt: This file is generated from index.py, which contains info of average length of documents, length of each document, information of fields as well as position of terms' posting list in postings.txt.
* postings.txt: This file is generated from index.py, which contains idf, doc_id, normalised weighted tf and position of each term in each document.
* BONUS.docx: This file contains query expansion techniques we have implemented

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] We, A0213835H-A0214251W-A0168291X-A0168954L, certify that we have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, we
expressly vow that we have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.

[ ] We, A0213835H-A0214251W-A0168291X-A0168954L, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

We suggest that we should be graded as follows:

<Please fill in>

== References ==