This is the README file for A0213835H's submission.

== Python Version ==

I'm using Python Version 3.7.6 for this assignment.

== General Notes about this assignment ==

I divide the whole program into four parts, a crawling part, a pagerank part, an index part and a search part. The crawling part is to crawl data from Wikipedia by using algorithm mentioned on the lecture. The pgerank part is to build the inverted index,
calculate and record the normalised weighted tfs corresponding to the postings and save the index into file. The indexer will
also save the term positions in the doc to aid with handling phrasal queries. The searcher loads the inverted index, parse
the query, search for all relevant documents in response to the query.

I adopt the object-oriented programming approach to build the whole project, which greatly reduces the coupling between four parts.

[Crawling]
As for the crawling part, there are two main functions to solve the problem.
    1. Get crawling rules from robots.txt
	1.1 Wget the robots.txt from https://en.wikipedia.org/robots.txt
	1.2 Fetch all Disallow link to the list
    2. Crawl Webpage
	2.1 Add a root link: https://en.wikipedia.org/wiki/Outline_of_computer_science to the frontier mentioned in the lecture
	2.2 Pop the frontier to get a url
	2.3 Fetch url and parse it
	2.4 Check the category of this webpage
	2.5 Fetch the title and content
	2.6 Check the content by using SimHash algorithm
	2.7 Add this url to fetchedurls
	2.8 Fetch all outlinks from this webpage
	2.9 For each outlink, obey the robots template and dup URL eliminates
	2.10 Add satisfied url into frontier
	2.11 Save url, title, content and outlinks to the file
	2.11 Loop 2.2-2.11 until reach max number of fetchedurls

[PageRank]
As for the pagerank part, there are two main functions to solve the problem.
    1. build and refine A matrix
	1.1 Get the shape of fetchedurl from crawling part to initiate A matrix
	1.2 When doing index part, for each file, get its outlinks to build A matrix
	1.3 After reading all files, refine A matrix by using Markov chains and Teleport methods

    2. Run pagerank algorithm to generate array a mentioned in the lecture

[Indexer]
As for the index part, there are two main functions to solve the problem.
    1. Build index
        1.1 Pre-process and store information about the zones (title)
            1.1.1 Remove all punctuations from title and content
            1.1.2 Stem the words and change all characters to lower case
            1.1.3 Append ".title" to words found in the title
            1.1.4 Add words to posting and store the doc id
            1.1.5 Store the position of each word in each document
	1.2 Process the term frequencies of each document
	    1.2.1 Normalise and weight the term frequencies
  	    1.2.2 Store resulting values in postings corresponding to each term and document
	1.3 Calculate average length of each document
	    1.3.1 Divide the sum of all lengths of documents by the number of documents

    2. Save to file
	2.1 For each term, save offset first
	2.2 Sort the postings list indexed by doc_id
	2.3 Split the total postings list into 3 parts: doc_id, 1+log(tf) and position
	2.4 Save three parts into postings file
	2.5 After saving terms, dump array a, average length of total docs, info of docs and dictionary into dictionary file

[Searcher]
As for the search part, I use the following steps to process a request.
    1. Tokenize the query into tokens, the program will also count the number of each term
       in the query.
    2. Load postings lists for the terms in the expression from the postings.txt file.
       For terms that appear multiple times in the query, I just load once to reduce memory cost.
       The postings lists include the docids, tfs and positions if the phrase query is turned on.
    3. Get the docs that need to rank.
       This step is mainly used to filter documents when phrase query is turned on.
       [phrasal query filtering]
	3.1 Get all the docs that contains all the terms in the query.
           Calculate the union of all postings lists, the searcher will merge them
           according to the size of the list.
       	3.2 Judging every doc whether it contains the phrase.
           After step 3.1, the candidate docs contain all terms but they may not adjacent.
           So I need to ensure the candidate docs contain the phrase.
    4. Rank the candidate docs and get the result.
       	4.1 Construct the query vector
           Based on the postings lists of terms, I can get the query vector.
       	4.2 Processing every document and every term.
           To get the cosine value of document vector and the query vector as doc's score.
       	4.3 Divide the score with the document length
           If the pivoted normalized document length is turned on, the score will be divided by the pivoted normalized document length.
	4.4 Use top 5 document to do the relevance feedback
       	4.5 Use max-head heap to get the K(can be set by user) most relevant docIds.
           If printing score is enabled, the scores will be returned too.
    5. Return the results

== Files included with this submission ==

* crawling.py: The file contains the Crawl class to crawl required webpages.
* pagerank.py: The file contains the PageRank class to build an A matrix and generate array a.
* index.py: The file in this assignment using Indexer to build the index and dump to file.
* indexer.py: The file contains the Indexer class which helps to build, load and dump the inverted index.
* search.py: The file in this assignment using Seacher to get all relevant documents.
* searcher.py: The file contains the Searcher class which helps to search the most relevant documents of the query.
* refiner.py: The file contains multiple methods for refining queries, like query expansion by synonyms and relevance feedback.
* dictionary.txt: This file is generated from index.py, which contains array a, info of average length of documents, length of each document, information of fields as well as position of terms' posting list in postings.txt.
* postings.txt: This file is generated from index.py, which contains idf, doc_id, normalised weighted tf and position of each term in each document.
* fetchedurls: This file is fetched urls generated after crawling webpages.
* queries.txt: This file contains several queried to be tested.
* output.txt: This file contains the result and corresponding urls from queries.txt.
* robots.txt: This file is the robots rules for crawling.
* simhash: This folder is external library for implementing simhash algorithm.
* webpages: This folder contains all crawl webpages.
* README.txt: This file contains an overview of this assignment and the algorithm's I used to solve it.
* DOC.pdf: This file contains some technologies I used for this project, like SimHash.
== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] I, A0213835H, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.

[ ] I, A0213835H, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

I suggest that I should be graded as follows:

* Complete all the requirements.
* Good programming habits, clear comments.
* Support additional command line arguments which is convenient to start various tests.
* Support phrasal query and pivoted normalized document length.
* Support query expansion and relevance feedback methods for refining queries
* Crawl wiki webpages for computer science and filter the content by multiple methods.
* Good performance:
  * Split the postings into three parts: doc_id, 1+log(tf) and position to index and search fast
  * Store the length(weight) of each doc when indexing, no need to recalculate it when searching
  * Avoid loading same term multiple times to save time and space.
  * Speed up merge when phrase is turned on.

== References ==
https://github.com/leonsim/simhash
https://github.com/cs-course-stu/CS3245-NUS-HW4
https://github.com/cs-course-stu/CS3245-NUS-HW3