try:
    import numpy
    import networkx
    import twitter
    import json
    import os
    import cPickle
    import nltk
    import codecs
    import sys
    import time

    #Random import to test for raising and catching an exception
    #import nonExistingModule

except ImportError as impErr:
    print ("Install the following from pypi before running this program:",impErr)
    print ("1. numpy")
    print ("2. networkx")
    print ("3. twitter")
    

class MiningTheSocialWebCh1(object):

    #Global variable to hold the filename in which to store the data obtained from the functions below
    fileName=''
    fileHandle=None



    def networkxGraphTrialRun(self):
        """
        This function just creates a random networkx graph.
        It does not serve any purpose other than to introduce the networkx module
        """
        myGraph=networkx.Graph()
        myGraph.add_edge(1,2)
        myGraph.add_node("spam")
        print (myGraph.nodes())
        print (myGraph.edges())


    def createAndOpenFile(self):
        """
        Just creates/opens a file for writing data to store in file
        """
        while self.fileHandle==None:
            if os.path.exists(self.fileName):
                print("File %s already exists, Overwriting it."%(self.fileName))
            
        
            try:
                self.fileHandle=open(self.fileName,'w')
                fileHandle=self.fileHandle
            except Exception as exception:
                print ("Failed to open the file %s"%(exception))
                returnValue = None
            else:
                returnValue = self.fileHandle
            # Don't forget to return the filehandler to the calling function, else you will be wondering
            # why self.fileHandle is 'None' there
            return returnValue

    def performNltkFrequencyAnalysis(self, words):
        frequencyDistribution=nltk.FreqDist(words)
        numOfWords=100
        print('%d most used words in the tweets are: %s'%(numOfWords,frequencyDistribution.keys()[:100]))
        print('%d least used words in the tweets are: %s'%(numOfWords,frequencyDistribution.keys()[-100:]))
        self.fileHandle.write('\n\n')
        self.fileHandle.write(str (numOfWords) + ' most used words in the tweets are: ' +str(frequencyDistribution.keys()[:100]))
        self.fileHandle.write('\n\n')
        self.fileHandle.write(str (numOfWords) + ' least used words in the tweets are: ' +str(frequencyDistribution.keys()[-100:]))
        self.fileHandle.write('\n\n')
        self.fileHandle.write('*'*80)

        self.fileHandle.close()

    def sendWordsToFile(self, words):
        fileHandle=open('myTwitterData.pickle','wb')
        cPickle.dump(words,fileHandle)
        fileHandle.close()
        words=cPickle.load(open('myTwitterData.pickle'))
        self.performNltkFrequencyAnalysis(words)
        


    def calculateLexicalDiversity(self, tweets):
        words=[]
        nos_of_tweets=0
        for t in tweets:
            words+=[w for w in t.split()]
            print (words)
            nos_of_tweets+=1
        self.fileHandle.write('\n\n')
        self.fileHandle.write ("nos of tweets is " + str(nos_of_tweets))
        self.fileHandle.write('\n\n')
        self.fileHandle.write ('Total number of words in all tweets analyzed: '+ str(len(words)))
        self.fileHandle.write('\n\n')
        self.fileHandle.write ('Total number of unique words in above tweets: '+ str(len(set(words))))
        self.fileHandle.write('\n\n')
        self.fileHandle.write ('Lexical diversity = '+ str(len(set(words))/float(len(words))))
        self.fileHandle.write('\n\n')
        #self.fileHandle.write ('Avg nos of words per tweet: '+ str(float(sum([ len(t.split()) for t in tweets ]))/float(len(words))))
        #self.fileHandle.write('\n\n')
        self.fileHandle.write ('Avg nos of words per tweet: '+ str(float(len(words))/nos_of_tweets))
        self.fileHandle.write('\n\n')
        self.fileHandle.write('*'*80)
        self.fileHandle.write('\n\n')
        self.sendWordsToFile(words)

        #fileHandle closed in nltk analysis


    def twitterAPITestStuff(self):
        """
        Operations on twitter as mentioned in 'Mining the social web chapter 1"
        """
        #The first 4 lines get the latest trends using the WOE(where on earth) id
        twitter_api=twitter.Twitter(domain="api.twitter.com", api_version='1')
        WORLD_WOE_ID = 1 # The Yahoo! Where On Earth ID for the entire world
        world_trends = twitter_api.trends._(WORLD_WOE_ID) 
        list_of_topics = [ trend['name'] for trend in world_trends()[0]['trends'] ] # iterate through the trends
        print (list_of_topics)  

        #This calls the search twitter for obtaining tweets on the topics obtained above
        twitter_search = twitter.Twitter(domain="search.twitter.com")
        all_search_results=[]
        search_results=[]
        
        self.fileName='TwitterCrapDataFromPythonAPI'+time.strftime("%Y%m%d-%H%M%S")
        self.fileHandle = self.createAndOpenFile()

        for topics in list_of_topics:
            print (topics)
            for page in range(1,5):
                #content = unicode(topics.strip(codecs.BOM_UTF8), 'utf-8')
                #parser.parse(StringIO.StringIO(content))
                #encoding to UTF-8 is essential because of internationalization which may show non-english words
                # output that are not parsable by urllib
                search_results.append(twitter_search.search(q=topics.encode("utf-8"),rpp=100, page=page))
                #Bandwidth forces me to use rpp=10...woule be better to use it as 100
                #print (search_results)
                #Output the entire json data to a file with proper formatting
                self.fileHandle.write (json.dumps(search_results, sort_keys=True, indent=1))
            #Strip only the tweets and show on the screen
            tweets=[ r['text'] \
                    for result in search_results \
                    for r in result['results']]
            print (tweets)
            self.fileHandle.write('\n\n\n\n\n')
            self.fileHandle.write('*'*80)
            #self.fileHandle.write(str(tweets))
        #Don't forget to colse the file opened above
        #self.fileHandle.close()
        #Closed in lexicaldiversity()
        self.calculateLexicalDiversity(tweets)

    def __init__(self):
        self.twitterAPITestStuff()
        reload(sys)
        sys.setdefaultencoding("utf-8")
        

def createInstanceForTesting():
    while True:
        classInstance=MiningTheSocialWebCh1()
        print ("Starting next round in 10s")
        time.sleep(10)

if __name__=='__main__':
    createInstanceForTesting()
    
