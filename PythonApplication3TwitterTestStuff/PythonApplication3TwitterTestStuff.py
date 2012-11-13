try:
    import numpy
    import networkx
    import twitter
    import json
    import os
    import cPickle
    import nltk
    import codecs

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
            #Don't fucking forget to return the filehandler to the calling function, else you will be wondering why self.fileHandle is 'None' there
            return returnValue

    def performNltkFrequencyAnalysis(self, words):
        frequencyDistribution=nltk.FreqDist(words)
        numOfWords=100
        print('%d most used words in the tweets are: %s'%(numOfWords,frequencyDistribution.keys()[:100]))
        print('%d least used words in the tweets are: %s'%(numOfWords,frequencyDistribution.keys()[-100:]))

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
        print ("nos of tweets is ", nos_of_tweets)

        print ('Total number of words in all tweets analyzed: ',len(words))
        print ('Total number of unique words in above tweets: ',len(set(words)))
        print ('Lexical diversity = ',len(set(words))/float(len(words)))
        print ('Avg nos of words per tweet: ',float(sum([ len(t.split()) for t in tweets ]))/float(len(words)))
        print ('Avg nos of words per tweet: ',float(len(words))/nos_of_tweets)

        self.sendWordsToFile(words)


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
        
        self.fileName='C:\TwitterCrapDataFromPythonAPI'
        self.fileHandle = self.createAndOpenFile()

        for topics in list_of_topics:
            print (topics)
            for page in range(1,5):
                #content = unicode(topics.strip(codecs.BOM_UTF8), 'utf-8')
                
                #parser.parse(StringIO.StringIO(content))
                search_results.append(twitter_search.search(q=topics,rpp=100, page=page))
                #print (search_results)
                #Output the entire json data to a file with proper formatting
                self.fileHandle.write (json.dumps(search_results, sort_keys=True, indent=1))
            #Strip only the tweets and show on the screen
            tweets=[ r['text'] \
                    for result in search_results \
                    for r in result['results']]
            print (tweets)
            self.fileHandle.write('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
            #self.fileHandle.write(str(tweets))
        #Don't forget to colse the file opened above
        self.fileHandle.close()
        self.calculateLexicalDiversity(tweets)

    



    def __init__(self):
        self.twitterAPITestStuff()

def createInstanceForTesting():
    classInstance=MiningTheSocialWebCh1()            

if __name__=='__main__':
    createInstanceForTesting()
