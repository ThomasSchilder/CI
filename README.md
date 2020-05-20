We used python 3.7

Instructions to run the algorithms:

For the content based algorithm you can run: python content-based.py

For the item based collaborative filtering algorithm you can run: python item-based-collab.py
In this file you can specity a userId. You can also specify with the boolean TEST if you want to run the test version.
In the test version we generate some tables and plots. If you run the testversion the userId is not used.

The item based algorithm uses pickles to store the similarity matrix etc for speedup.
If you already have the pickles, you can type yes. Then the similarity matrix isn't regenerated.
If you type no, it will try to generate a similarity matrix based on the "data" folder. So you need to copy Yelp data in this folder.