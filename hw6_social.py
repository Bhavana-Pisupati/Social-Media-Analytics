"""
Social Media Analytics Project
Name:
Roll Number:
"""

import hw6_social_tests as test

project = "Social" # don't edit this

### PART 1 ###

import pandas as pd
import nltk
nltk.download('vader_lexicon', quiet=True)
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
endChars = [ " ", "\n", "#", ".", ",", "?", "!", ":", ";", ")" ]

'''
makeDataFrame(filename)
#3 [Check6-1]
Parameters: str
Returns: dataframe
'''
def makeDataFrame(filename):
    df=pd.read_csv(filename)
    return df


'''
parseName(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parseName(fromString):
    start=(fromString.find("From"))+len("From:")
    fromString=fromString[start:]
    end=fromString.find("(")
    fromString=fromString[:end]
    fromString=fromString.strip()
    return fromString


'''
parsePosition(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parsePosition(fromString):
    start=fromString.find("(")+1
    fromString=fromString[start:]
    end=fromString.find("from")
    fromString=fromString[:end]
    fromString=fromString.strip()
    return fromString


'''
parseState(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parseState(fromString):
    start=(fromString.find("from"))+len("from ")
    fromString=fromString[start:]
    end=fromString.find(")")
    fromString=fromString[:end]
    fromString=fromString.strip()
    return fromString


'''
findHashtags(message)
#5 [Check6-1]
Parameters: str
Returns: list of strs
'''
def findHashtags(message):
    tags=[]
    count=message.count("#")
    for i in range(count):
        start=message.find("#")
        message=message[start:]
        s=message[1:]
        end=len(s)+1
        for j in range(len(s)):
            if s[j] in endChars:
                end=j+1
                break         
        tag=message[:end]
        message=message[1:]
        tags.append(tag)
    return tags

    # return message


'''
getRegionFromState(stateDf, state)
#6 [Check6-1]
Parameters: dataframe ; str
Returns: str
'''
def getRegionFromState(stateDf, state):
    row=stateDf.loc[stateDf['state'] == state, 'region']
    return row.values[0]


'''
addColumns(data, stateDf)
#7 [Check6-1]
Parameters: dataframe ; dataframe
Returns: None
'''
def addColumns(data, stateDf):
    names=[]
    positions=[]
    states=[]
    regions=[]
    hashtags=[]
    for index,row in data.iterrows():
        value=row['label']
        names.append(parseName(value))
        positions.append(parsePosition(value))
        states.append(parseState(value))
        regions.append(getRegionFromState(stateDf,parseState(value)))
        text=row['text']
        hashtags.append(findHashtags(text))
    data['name']=names
    data['position']=positions
    data['state']=states
    data['region']=regions
    data['hashtags']=hashtags


### PART 2 ###

'''
findSentiment(classifier, message)
#1 [Check6-2]
Parameters: SentimentIntensityAnalyzer ; str
Returns: str
'''
def findSentiment(classifier, message):
    score = classifier.polarity_scores(message)['compound']
    if score<-0.1:
        return "negative"
    elif score>0.1:
        return "positive"
    else:
        return "neutral"


'''
addSentimentColumn(data)
#2 [Check6-2]
Parameters: dataframe
Returns: None
'''
def addSentimentColumn(data):
    classifier = SentimentIntensityAnalyzer()
    sentiments=[]
    for index,row in data.iterrows():
        text=row['text']
        sentiments.append(findSentiment(classifier,text))
    data['sentiment']=sentiments


'''
getDataCountByState(data, colName, dataToCount)
#3 [Check6-2]
Parameters: dataframe ; str ; str
Returns: dict mapping strs to ints
'''
def getDataCountByState(data, colName, dataToCount):
    d={}
    for index,row in data.iterrows():
        if colName=="" and dataToCount=="":
            if row['state'] not in d:
                d[row['state']]=0
            d[row['state']]+=1
        elif row[colName]==dataToCount:
            if row['state'] not in d:
                d[row['state']]=0
            d[row['state']]+=1
    return d


'''
getDataForRegion(data, colName)
#4 [Check6-2]
Parameters: dataframe ; str
Returns: dict mapping strs to (dicts mapping strs to ints)
'''
def getDataForRegion(data, colName):
    d={}
    for index,row in data.iterrows():
        if row['region'] not in d:
            d[row['region']]={}
        if row[colName] not in d[row['region']]:
            d[row['region']][row[colName]]=0
        d[row['region']][row[colName]]+=1       
    return d


'''
getHashtagRates(data)
#5 [Check6-2]
Parameters: dataframe
Returns: dict mapping strs to ints
'''
def getHashtagRates(data):
    d={}
    for index,row in data.iterrows():
        for i in row['hashtags']:
            if i not in d:
                d[i]=0
            d[i]+=1       
    return d


'''
mostCommonHashtags(hashtags, count)
#6 [Check6-2]
Parameters: dict mapping strs to ints ; int
Returns: dict mapping strs to ints
'''
def mostCommonHashtags(hashtags, count):
    d={}
    while len(d)<count:
        max=0
        for i in hashtags:
            if i not in d:
                if hashtags[i]>max:
                    max=hashtags[i]
                    tag=i
        d[tag]=max
    return d


'''
getHashtagSentiment(data, hashtag)
#7 [Check6-2]
Parameters: dataframe ; str
Returns: float
'''
def getHashtagSentiment(data, hashtag):
    score=0
    count=0
    for index,row in data.iterrows():
        if hashtag in findHashtags(row['text']):
            value=row['sentiment']
            if value=='positive':
                score+=1
            if value=='negative':
                score-=1
            if value=='neutral':
                score=score+0
            count+=1
    return score/count


### PART 3 ###

'''
graphStateCounts(stateCounts, title)
#2 [Hw6]
Parameters: dict mapping strs to ints ; str
Returns: None
'''
def graphStateCounts(stateCounts, title):
    import matplotlib.pyplot as plt
    x=stateCounts.keys()
    y=stateCounts.values()
    plt.bar(x,y)
    plt.xticks(rotation='vertical')
    plt.title(title)
    plt.show()


'''
graphTopNStates(stateCounts, stateFeatureCounts, n, title)
#3 [Hw6]
Parameters: dict mapping strs to ints ; dict mapping strs to ints ; int ; str
Returns: None
'''
def graphTopNStates(stateCounts, stateFeatureCounts, n, title):
    freqdict={}
    for i in stateCounts:
        if i in stateFeatureCounts:
            frequency=stateFeatureCounts[i]/stateCounts[i]
            freqdict[i]=frequency
    d={}
    while len(d)<n:
        max=0
        for i in freqdict:
            if i not in d:
                if freqdict[i]>max:
                    max=freqdict[i]
                    tag=i
        d[tag]=max
    x=d.keys()
    y=d.values()
    plt.bar(x,y)
    plt.title(title)
    plt.show()



'''
graphRegionComparison(regionDicts, title)
#4 [Hw6]
Parameters: dict mapping strs to (dicts mapping strs to ints) ; str
Returns: None
'''
def graphRegionComparison(regionDicts, title):
    featureslist=[]
    regionslist=[]
    regionfeaturelists=[]
    for i in regionDicts:
        for j in regionDicts[i]:
            if j not in featureslist:
                featureslist.append(j)
    for i in regionDicts.keys():
        regionslist.append(i)
    for i in regionDicts:
        list=[]
        for j in featureslist:
            index=0
            for k in regionDicts[i]:
                if k==j:
                    index+=regionDicts[i][k]
            list.append(index)
        regionfeaturelists.append(list)
    sideBySideBarPlots(featureslist, regionslist, regionfeaturelists, title)


'''
graphHashtagSentimentByFrequency(data)
#4 [Hw6]
Parameters: dataframe
Returns: None
'''
def graphHashtagSentimentByFrequency(data):
    hashtag=getHashtagRates(data)
    hashtags=[]
    scores=[]
    frequencies=[]
    d=mostCommonHashtags(hashtag, 50)
    for i in d:
        score=getHashtagSentiment(data, i)
        frequencies.append(d[i])
        scores.append(score)
        hashtags.append(i)
    scatterPlot(frequencies,scores,hashtags,"HashtagSentiments to frequencies")
    return


#### PART 3 PROVIDED CODE ####
"""
Expects 3 lists - one of x labels, one of data labels, and one of data values - and a title.
You can use it to graph any number of datasets side-by-side to compare and contrast.
"""
def sideBySideBarPlots(xLabels, labelList, valueLists, title):
    import matplotlib.pyplot as plt

    w = 0.8 / len(labelList)  # the width of the bars
    xPositions = []
    for dataset in range(len(labelList)):
        xValues = []
        for i in range(len(xLabels)):
            xValues.append(i - 0.4 + w * (dataset + 0.5))
        xPositions.append(xValues)

    for index in range(len(valueLists)):
        plt.bar(xPositions[index], valueLists[index], width=w, label=labelList[index])

    plt.xticks(ticks=list(range(len(xLabels))), labels=xLabels, rotation="vertical")
    plt.legend()
    plt.title(title)

    plt.show()

"""
Expects two lists of probabilities and a list of labels (words) all the same length
and plots the probabilities of x and y, labels each point, and puts a title on top.
Expects that the y axis will be from -1 to 1. If you want a different y axis, change plt.ylim
"""
def scatterPlot(xValues, yValues, labels, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    plt.scatter(xValues, yValues)

    # make labels for the points
    for i in range(len(labels)):
        plt.annotate(labels[i], # this is the text
                    (xValues[i], yValues[i]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0, 10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    plt.title(title)
    plt.ylim(-1, 1)

    # a bit of advanced code to draw a line on y=0
    ax.plot([0, 1], [0.5, 0.5], color='black', transform=ax.transAxes)

    plt.show()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    # print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    # test.week1Tests()
    # print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    # test.runWeek1()
    # test.testMakeDataFrame()
    # test.testParseName()
    # test.testParsePosition()
    # test.testParseState()
    # test.testFindHashtags()
    # test.testGetRegionFromState()
    # test.testAddColumns()
    
    ## Uncomment these for Week 2 ##
    # print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    # test.week2Tests()
    # print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    # test.runWeek2()
    # test.testFindSentiment()
    # test.testAddSentimentColumn()

    # df = makeDataFrame("data/politicaldata.csv")
    # stateDf = makeDataFrame("data/statemappings.csv")
    # addColumns(df, stateDf)
    # addSentimentColumn(df)

    # test.testGetDataCountByState(df)
    # test.testGetDataForRegion(df)
    # test.testGetHashtagRates(df)
    # test.testMostCommonHashtags(df)
    # test.testGetHashtagSentiment(df)


    ## Uncomment these for Week 3 ##
    # print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    test.runWeek3()
