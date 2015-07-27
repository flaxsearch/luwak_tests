==========================================================
Luwak performance comparison with Elasticsearch Percolator
==========================================================

This directory contains some simple programs for comparing the performance of the Luwak
query engine from Flax [1] with the Percolator feature of Elasticsearch [2]. 

These instructions assume you are working on OS X or Linux. It should be straightforward
to make this work on Windows by making suitable adaptations and/or using Cygwin [5].


-----------
Prequisites
-----------

The following packages must first be installed on your system:

- Java 8.x
- Apache Maven 3.x
- Python 2.7
- Python requests [3]
- Scrapy 1.x [4]
- Luwak (master-5.1 branch) [1]
- Elasticsearch 1.6.x [2]
- curl

The amount of RAM required depends on the size and kind of tests you are planning to
run, but we would recommend a minumum of 8GB. Running any other demanding applications
at the same time as the tests will distort the results. 


-------------------
Building luwak_test
-------------------

Once Luwak is installed, building the test app should be as simple as:

    $ cd luwak_test
    $ mvn clean package

This will create luwak_test-0.0.1-SNAPSHOT.jar in luwak_test/target.


--------------------------
Downloading test documents
--------------------------

The download-random-wp-text.py script downloads random articles from Wikipedia. It takes
two parameters, the number of articles to download and the document in which to save them.
e.g.:

    $ mkdir docs
    $ python download-random-wp-text.py 1000 docs

This will download 1000 random articles and save the text as .gz files in docs/. 


-----------------------
Creating random queries
-----------------------

The generate-queries.py script can be used to generate random queries in Lucene query 
parser format. It uses the downloaded documents as input, and attempts to generate 
"reaslistic" queries (in the sense that they will match some documents). The following 
query types are supported:

    - Boolean queries combining MUST and NOT terms, e.g.:
        
        +northward +since +september -survey -earned
    
    - The same, with wildcard terms:

        +nort* +sinc* +sept* -surv* -earn*
    
    - Two-term phrase query with slop:
    
        "environment variable"~5
    
The number of MUST and NOT terms, the wildcard prefix length, and the phrase slop are
all configurable on the command line. Queries are output as separate files in the
specified directory. For example, to create 5000 queries with 100 MUST terms and 25 NOT 
terms:

    $ python generate-queries.py --count=5000 --docdir=docs --querydir=queries \
                                 --MUST=100 --NOT=25

To generate the same, with a wildcard terms with a prefix length of three characters:    

    $ python generate-queries.py --count=5000 --docdir=docs --querydir=queries \
                                 --MUST=100 --NOT=25 --wild=3

To generate 5000 phrase queries with a slop of 7:

    $ python generate-queries.py --count=5000 --docdir=docs --querydir=queries \
                                 --within=7


---------------------------
Running Elasticsearch tests
---------------------------

If you do not have Elasticsearch running on localhost, edit the ES_URL parameter in 
conf.py. Before indexing the queries into Percolator, you must create the 'test'
index with the appropriate settings. Run:

    $ ./reset-es-test-index.sh

This also deletes any existing 'test' index, so you can use it between test runs to
clear the data.

Before percolating documents, you need to index the queries. To do that, run 
the following command (substituting the appropriate query directory):

    $ python es-index-percolator.py queries

Once the queries have been indexed, you can percolate documents with the command 
(substituting the appropriate documents directory):

    $ python es-percolate-docs.py docs

Percolation can be slow. Accordingly, if you want to terminate the script after a 
certain number of documents, add this limit as a parameter:

    $ python es-percolate-docs.py docs 2000

After processing the documents, this script will report the mean documents per second
percolated.


-------------------
Running Luwak tests
-------------------

The Luwak test app loads the queries into an in-memory index before processing the 
documents. It does not include this load time in the documents-per-second calculation,
since query load time will be an insignificant overhead in any long-running monitor
application (it is also possible to store the index on disk similarly to Percolator).

To run the test app, give it the location of the query directory and document 
directory, e.g.:

    $ java -Xms4G -jar luwak_test/target/luwak_test-0.0.1-SNAPSHOT.jar \
           queries documents

As with the Elasticsearch script, you can limit the number of documents processed:

    $ java -Xms4G -jar luwak_test/target/luwak_test-0.0.1-SNAPSHOT.jar \
           queries documents 2000

For the sake of fairness, you should run the same number of documents through Percolator
and Luwak for each test, and give Elasticsearch and Luwak the same Java heap size.


--
Author: Tom Mortimer <tom@flax.co.uk>

[1]  https://github.com/flaxsearch/luwak/tree/master-5.1
[2]  https://www.elastic.co/guide/en/elasticsearch/reference/current/search-percolate.html
[3]  http://docs.python-requests.org/en/latest/
[4]  http://doc.scrapy.org/en/latest/intro/install.html
[5]  https://www.cygwin.com
