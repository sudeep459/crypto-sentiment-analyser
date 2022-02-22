# Required imports
import pandas as pd
import spacy
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup
from pymongo import MongoClient
from nltk import ngrams
from urllib.request import Request, urlopen
import requests
import json 
import re

from config import *
#################
## WEBSCRAPING ##
#################

def scrapeArticles():
    
    CLEANR = re.compile('<.*?>') 
    link = "https://www.cryptonext.ai/wp-json/wp/v2/posts"
    coin_list = ['bitcoin', 'altcoin', 'ethereum', 'ripple', 'shiba-inu', 'dogecoin', 'cardano', 'polkadot', 'solana', 'tether']
    coins = []
    titles = []
    shortdesc = []
    times = []
    links = []
    desc = []
    ids = []
    
    try:
        req = Request(link, headers= {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50"})
        webpage = urlopen(req).read()
        with requests.Session() as c:
            soup = BeautifulSoup(webpage, 'html5lib')
        body = soup.find('body')
        articles = json.loads(body.text)
    except Exception as e:
        print(e)

    for article in articles:
        try:
            artid = article['id'] 
            date = article['date'].split('T')[0]
            title = article['title']['rendered']
            sd = article['excerpt']['rendered']
            des = article['content']['rendered']
            des = re.sub(CLEANR, '', des)
            desn = des.split()
            desnew = ''
            for item in desn[:-3]:
                desnew = desnew + " " + item
            link = article['_links']['self'][0]['href']
            coinlink = article['_links']['wp:term'][0]['href']
            req = Request(coinlink, headers= {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50"})
            webpage = urlopen(req).read()
            soup1 = BeautifulSoup(webpage, 'html5lib')
            body1 = soup1.find('body')
            js = json.loads(body1.text)
            coinname = js[0]['slug']
            if coinname not in coin_list:
                continue
            ids.append(artid)
            coins.append(coinname)
            links.append(link)
            desc.append(desnew)
            shortdesc.append(sd)
            titles.append(title)
            times.append(date)
        except Exception as e:
            print(e)
    
    data = {'ArticleID': ids, 'Coin': coins, 'Title' : titles, 'Shortdescription' : shortdesc, 'Time' : times, 'Link' : links, 'Description' : desc}
    df = pd.DataFrame(data)
    
    print("Done scraping")
    return df

def take_second(elem):
    return elem['score']

###############################################
## Get Named Entities and Sentiment Analysis ##
###############################################

def ner_and_sentiment(df):
    
    nlp = spacy.load('en_core_web_sm')
    
    df = df

    title_ents = []
    desc_ents = []
    
    for i in range(0,len(df)):
        row = df.iloc[i]
        tdoc = nlp(str(row.Title))
        ddoc = nlp(str(row.Description))
        tents = []
        dents  = []
        if tdoc.ents:
            for ent in tdoc.ents:
                element = ''
                element = element + ent.text + ' - ' + ent.label_
                tents.append(element)
        else:
            tents.append('No entities Found')
        if ddoc.ents:
            for ent in ddoc.ents:
                element = ''
                element = element + ent.text + ' - ' + ent.label_
                dents.append(element)
        else:
            dents.append('No entities Found')
        title_ents.append(tents)
        desc_ents.append(dents)

    df['Title_Ents'] = title_ents
    df['Description_Ents'] = desc_ents

    sid = SentimentIntensityAnalyzer()

    scores = []
    for i,artid,c,t,sd,tim,l,d,tent,dent in df.itertuples():
            score = sid.polarity_scores(str(d))
            scores.append(score)

    df['scores'] = scores

    df['score'] = df['scores'].apply(lambda d:d['compound'])
    df['Overall_bias'] = df['score'].apply(lambda score: 'Positive' if score > 0.5 else 'Negative' if score < -0.5 else 'Neutral')
    df.drop('scores', axis = 1, inplace = True)
    
    oneword_list = []
    twoword_list = []
    threeword_list = []
    for i,artid,c,t,sd,ti,l,d,te,de,s,b in df.itertuples():
        pos_word_list=[]
        neu_word_list=[]
        neg_word_list=[] 
        n = 2
        bigrams = ngrams(d.split(), n)
        n = 3
        trigrams = ngrams(d.split(), n)
        onegrams = d.split()

        for word in onegrams:                                 ###### Single words ###########
            
            if nlp.vocab[word.lower()].is_stop != True: 
                score = sid.polarity_scores(word)['compound']
                if score > 0.2:
                    if {"words":[word],"score": score} in pos_word_list:
                        continue
                    else:
                        pos_word_list.append({'words': [word],'score': score})
                elif score < -0.2:
                    if {"words":[word],"score": score} in neg_word_list:
                        continue
                    else:
                        neg_word_list.append({'words': [word],'score': score})
                else:
                    if {"words":[word],"score": score} in neu_word_list:
                        continue
                    else:
                        neu_word_list.append({'words': [word],'score': score})  
        pos_word_list = sorted(pos_word_list, key = take_second, reverse = True)
        neg_word_list = sorted(neg_word_list, key = take_second)
        neu_word_list = sorted(neu_word_list, key = take_second)
    
        if b == 'Positive':
            oneword_list.append(pos_word_list[:5])
        elif b == 'Negative':
            oneword_list.append(neg_word_list[:5])
        else:
            oneword_list.append(neu_word_list[:5])
        
        pos_word_list=[]
        neu_word_list=[]
        neg_word_list=[]
        
        for word in bigrams:                                   ###### Bigrams ########### 
                temp = []
                temp.append(word[0])
                temp.append(word[1])
                s = word[0] + ' ' + word[1]
                score = sid.polarity_scores(s)['compound']
                if score > 0.2:
                    pos_word_list.append({'words': temp,'score': score})
                elif score < -0.2:
                    neg_word_list.append({'words': temp,'score': score})
                else:
                    neu_word_list.append({'words': temp,'score': score})    
        pos_word_list = sorted(pos_word_list, key = take_second, reverse = True)
        neg_word_list = sorted(neg_word_list, key = take_second)
        neu_word_list = sorted(neu_word_list, key = take_second)
        
        if b == 'Positive':
            twoword_list.append(pos_word_list[:5])
        elif b == 'Negative':
            twoword_list.append(neg_word_list[:5])
        else:
            twoword_list.append(neu_word_list[:5])
        
        pos_word_list=[]
        neu_word_list=[]
        neg_word_list=[]
        
        
        for word in trigrams:                                   ###### Trigrams ###########
                temp = []
                temp.append(word[0])
                temp.append(word[1])
                temp.append(word[2])
                s = word[0] + ' '+ word [1] + ' '+ word[2]
                score = sid.polarity_scores(s)['compound']
                if score > 0.2:
                    pos_word_list.append({'words': temp,'score': score})
                elif score < -0.2:
                    neg_word_list.append({'words': temp,'score': score})
                else:
                    neu_word_list.append({'words': temp,'score': score}) 
        
        pos_word_list = sorted(pos_word_list, key = take_second, reverse = True)
        neg_word_list = sorted(neg_word_list, key = take_second)
        neu_word_list = sorted(neu_word_list, key = take_second)
        
        if b == 'Positive':
            threeword_list.append(pos_word_list[:5])
        elif b == 'Negative':
            threeword_list.append(neg_word_list[:5])
        else:
            threeword_list.append(neu_word_list[:5])
        
    df['One_word_Reviews'] = [el for el in oneword_list]
    df['Two_word_Reviews'] = [el for el in twoword_list]
    df['Three_word_Reviews'] = [el for el in threeword_list]
    print('Done with sentiment analysis')
    return df

###################
##APPEND TO MONGO##
###################

# Change url
 
def addtodb(df):
    url = MONGO_URL
    client = MongoClient(url)
    db = client['crypto-news']
    collection = db['inventory']
    if len(df) != 0:
        for doc in df.to_dict('records'):
            collection.update_one({'ArticleID': doc['ArticleID']}, {"$set": doc}, upsert = True)
    print("Added to db")

##########
## MAIN ##
##########

def main():
    
    df = scrapeArticles()
    df = ner_and_sentiment(df)
    addtodb(df)    
if __name__ == "__main__":
    main()

