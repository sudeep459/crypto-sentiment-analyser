# Required imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import spacy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup
import datetime
from time import sleep
from pymongo import MongoClient
from nltk import ngrams


#################
## WEBSCRAPING ##
#################

def scrapeArticles(coin):
    
    nlp = spacy.load('en_core_web_sm')
    PATH = '/usr/lib/chromium-browser/chromedriver'
    options = webdriver.ChromeOptions()
    options.headless = True

    driver = webdriver.Chrome(PATH, options = options)  
    driver.get(f"https://coinmarketcap.com/currencies/{coin}/news/")
    driver.maximize_window()

    titles = []
    desc = []
    age = []
    links = []
    sources = []
    
    try:

        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div[2]/div/div[3]/div/div/main/div[2]'))
        )
        articles = main.find_elements(By.XPATH, 'div')
        while(True):
            try:
                driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div[2]/div/div[3]/div/div/main/button'))))
            except:
                break
            articles = main.find_elements(By.XPATH, 'div')
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            els = soup.find_all('span', attrs={'class' : 'sc-1eb5slv-0 hykWbK'})
            l_time = els[-1].text
            if l_time.find('days') != -1:
                break
            elif l_time.find('month') != -1:
                break
            else:
                continue
        for article in articles:
            try:
                element = WebDriverWait(article, 10).until(
                    EC.presence_of_element_located((By.XPATH, 'a/div[1]'))
                )
                source = element.find_element(By.XPATH,'div/span[1]')
                link = article.find_element(By.XPATH, 'a').get_attribute('href')
                title = element.find_element(By.XPATH, 'h3')
                body = element.find_element(By.XPATH, 'p').text.split('...')
                time = element.find_element(By.XPATH, 'div/span[2]').text
                if time.find('days') != -1:
                    continue
                elif time.find('day') != -1:
                    titles.append(title.text)
                    desc.append(body[0])
                    t = datetime.datetime.now() - datetime.timedelta(days = 1)
                    sttime = t.strftime('%Y-%m-%d')
                    age.append(sttime)
                    links.append(link)
                    sources.append(source.text)
                else:
                    continue
            except:
                continue
        c = []
        for i in range(0,len(titles)):
            c.append(coin)
        data = {'Coin': c, 'Title' : titles, 'Shortdescription' : desc, 'Time' : age, 'Link' : links, 'Source': sources}
        df = pd.DataFrame(data)
    finally:
        driver.quit()

    driver = webdriver.Chrome(PATH, options = options)
    
    desc = []
    for i,link in enumerate(links):
        driver.get(link)
        sleep(2)
        try:
            al = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div[2]/a'))
                ).get_attribute('href')
            driver.get(al)
            sleep(2)
        except:
            print('no reroute')
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        descr = soup.find_all('p')
        st = ''
        for p in descr:
            doc = nlp(p.text)
            if len(doc) > 2:
                txt = p.text.lower()
                if (txt.find('cookie') == -1 & txt.find('create a free account') == -1 & txt.find('subscribe')== -1 & txt.find("thanks for reading")== -1):
                    st = st + p.text + ' '
        source = df.iloc[i]['Source']
        if source == 'Seeking Alpha':
            desc.append(df.iloc[i]['Shortdescription'])
        else:
            desc.append(st)
    driver.quit()
    df.drop('Source', axis = 1, inplace = True)
    df['Description'] = desc
    
    return df

def take_second(elem):
    return elem[1]

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
    for i,c,t,sd,tim,l,d,tent,dent in df.itertuples():
            score = sid.polarity_scores(str(d))
            scores.append(score)

    df['scores'] = scores

    df['score'] = df['scores'].apply(lambda d:d['compound'])
    df['Overall_bias'] = df['score'].apply(lambda score: 'Positive' if score > 0.5 else 'Negative' if score < -0.5 else 'Neutral')
    df.drop('scores', axis = 1, inplace = True)
    
    oneword_list = []
    twoword_list = []
    threeword_list = []
    for i,c,t,sd,ti,l,d,te,de,s,b in df.itertuples():
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
                    if (word,score) in pos_word_list:
                        continue
                    else:
                        pos_word_list.append((word,score))
                elif score < -0.2:
                    if (word,score) in neg_word_list:
                        continue
                    else:
                        neg_word_list.append((word,score))
                else:
                    if (word,score) in neu_word_list:
                        continue
                    else:
                        neu_word_list.append((word,score))  
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
                   
                s = word[0] + ' ' + word[1]
                score = sid.polarity_scores(s)['compound']
                if score > 0.2:
                    pos_word_list.append((s,score))
                elif score < -0.2:
                    neg_word_list.append((s,score))
                else:
                    neu_word_list.append((s,score))    
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
                s = word[0] + ' '+ word [1] + ' '+ word[2]
                score = sid.polarity_scores(s)['compound']
                if score > 0.2:
                    pos_word_list.append((s,score))
                elif score < -0.2:
                    neg_word_list.append((s,score))
                else:
                    neu_word_list.append((s,score)) 
        
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
    return df

###################
##APPEND TO MONGO##
###################

# Change url
 
def addtodb(df):
    url = ''
    client = MongoClient(url)
    db = client['crypto-news']
    collection = db['inventory']
    if len(df) != 0:
        collection.insert_many(df.to_dict('records'))

##########
## MAIN ##
##########

def main():
    coins = ['bitcoin', 'ethereum', 'dogecoin', 'litecoin', 'bnb']
    for coin in coins:
        dat = scrapeArticles(coin)
        dat = ner_and_sentiment(dat)
        addtodb(dat)
    
if __name__ == "__main__":
    main()

