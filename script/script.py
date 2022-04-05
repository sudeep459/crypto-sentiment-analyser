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
    symbols = []
    res = {"cryptocurrencies":[{"Name":"Bitcoin","Symbol":"BTC"},{"Name":"Ethereum","Symbol":"ETH"},{"Name":"BNB","Symbol":"BNB"},{"Name":"Tether","Symbol":"USDT"},{"Name":"Cardano","Symbol":"ADA"},{"Name":"USD Coin","Symbol":"USDC"},{"Name":"Solana","Symbol":"SOL"},{"Name":"XRP","Symbol":"XRP"},{"Name":"Terra","Symbol":"LUNA"},{"Name":"Polkadot","Symbol":"DOT"},{"Name":"Dogecoin","Symbol":"DOGE"},{"Name":"Avalanche","Symbol":"AVAX"},{"Name":"Polygon","Symbol":"MATIC"},{"Name":"Shiba Inu","Symbol":"SHIB"},{"Name":"Binance USD","Symbol":"BUSD"},{"Name":"NEAR Protocol","Symbol":"NEAR"},{"Name":"Chainlink","Symbol":"LINK"},{"Name":"Crypto.com Coin","Symbol":"CRO"},{"Name":"Wrapped Bitcoin","Symbol":"WBTC"},{"Name":"TerraUSD","Symbol":"UST"},{"Name":"Uniswap","Symbol":"UNI"},{"Name":"Litecoin","Symbol":"LTC"},{"Name":"Dai","Symbol":"DAI"},{"Name":"Cosmos","Symbol":"ATOM"},{"Name":"Algorand","Symbol":"ALGO"},{"Name":"Fantom","Symbol":"FTM"},{"Name":"TRON","Symbol":"TRX"},{"Name":"Bitcoin Cash","Symbol":"BCH"},{"Name":"FTX Token","Symbol":"FTT"},{"Name":"Stellar","Symbol":"XLM"},{"Name":"Internet Computer","Symbol":"ICP"},{"Name":"Decentraland","Symbol":"MANA"},{"Name":"Hedera","Symbol":"HBAR"},{"Name":"Axie Infinity","Symbol":"AXS"},{"Name":"VeChain","Symbol":"VET"},{"Name":"Bitcoin BEP2","Symbol":"BTCB"},{"Name":"The Sandbox","Symbol":"SAND"},{"Name":"Filecoin","Symbol":"FIL"},{"Name":"Ethereum Classic","Symbol":"ETC"},{"Name":"Monero","Symbol":"XMR"},{"Name":"Theta Network","Symbol":"THETA"},{"Name":"Harmony","Symbol":"ONE"},{"Name":"Elrond","Symbol":"EGLD"},{"Name":"Tezos","Symbol":"XTZ"},{"Name":"Klaytn","Symbol":"KLAY"},{"Name":"UNUS SED LEO","Symbol":"LEO"},{"Name":"Helium","Symbol":"HNT"},{"Name":"Aave","Symbol":"AAVE"},{"Name":"IOTA","Symbol":"MIOTA"},{"Name":"PancakeSwap","Symbol":"CAKE"},{"Name":"EOS","Symbol":"EOS"},{"Name":"Stacks","Symbol":"STX"},{"Name":"The Graph","Symbol":"GRT"},{"Name":"BitTorrent","Symbol":"BTT"},{"Name":"Flow","Symbol":"FLOW"},{"Name":"Kusama","Symbol":"KSM"},{"Name":"Gala","Symbol":"GALA"},{"Name":"Curve DAO Token","Symbol":"CRV"},{"Name":"Maker","Symbol":"MKR"},{"Name":"Bitcoin SV","Symbol":"BSV"},{"Name":"Enjin Coin","Symbol":"ENJ"},{"Name":"THORChain","Symbol":"RUNE"},{"Name":"Quant","Symbol":"QNT"},{"Name":"eCash","Symbol":"XEC"},{"Name":"Zcash","Symbol":"ZEC"},{"Name":"Celo","Symbol":"CELO"},{"Name":"Oasis Network","Symbol":"ROSE"},{"Name":"Amp","Symbol":"AMP"},{"Name":"Neo","Symbol":"NEO"},{"Name":"KuCoin Token","Symbol":"KCS"},{"Name":"OKB","Symbol":"OKB"},{"Name":"Loopring","Symbol":"LRC"},{"Name":"Chiliz","Symbol":"CHZ"},{"Name":"Arweave","Symbol":"AR"},{"Name":"Basic Attention Token","Symbol":"BAT"},{"Name":"Huobi Token","Symbol":"HT"},{"Name":"Waves","Symbol":"WAVES"},{"Name":"TrueUSD","Symbol":"TUSD"},{"Name":"Dash","Symbol":"DASH"},{"Name":"Kadena","Symbol":"KDA"},{"Name":"Secret","Symbol":"SCRT"},{"Name":"Nexo","Symbol":"NEXO"},{"Name":"Mina","Symbol":"MINA"},{"Name":"yearn.finance","Symbol":"YFI"},{"Name":"Compound","Symbol":"COMP"},{"Name":"IoTeX","Symbol":"IOTX"},{"Name":"XDC Network","Symbol":"XDC"},{"Name":"Holo","Symbol":"HOT"},{"Name":"NEM","Symbol":"XEM"},{"Name":"1inch Network","Symbol":"1INCH"},{"Name":"Ravencoin","Symbol":"RVN"},{"Name":"Pax Dollar","Symbol":"USDP"},{"Name":"Theta Fuel","Symbol":"TFUEL"},{"Name":"Decred","Symbol":"DCR"},{"Name":"OMG Network","Symbol":"OMG"},{"Name":"SushiSwap","Symbol":"SUSHI"},{"Name":"Kava","Symbol":"KAVA"},{"Name":"Bancor","Symbol":"BNT"},{"Name":"BORA","Symbol":"BORA"},{"Name":"Zilliqa","Symbol":"ZIL"},{"Name":"Qtum","Symbol":"QTUM"},{"Name":"WAX","Symbol":"WAXP"},{"Name":"APENFT","Symbol":"NFT"},{"Name":"WOO Network","Symbol":"WOO"},{"Name":"Velas","Symbol":"VLX"},{"Name":"renBTC","Symbol":"RENBTC"},{"Name":"Celsius","Symbol":"CEL"},{"Name":"Ankr","Symbol":"ANKR"},{"Name":"Livepeer","Symbol":"LPT"},{"Name":"Syscoin","Symbol":"SYS"},{"Name":"Immutable X","Symbol":"IMX"},{"Name":"Audius","Symbol":"AUDIO"},{"Name":"Dogelon Mars","Symbol":"ELON"},{"Name":"Gnosis","Symbol":"GNO"},{"Name":"ICON","Symbol":"ICX"},{"Name":"Voyager Token","Symbol":"VGX"},{"Name":"Revain","Symbol":"REV"},{"Name":"Siacoin","Symbol":"SC"},{"Name":"Horizen","Symbol":"ZEN"},{"Name":"Bitcoin Gold","Symbol":"BTG"},{"Name":"0x","Symbol":"ZRX"},{"Name":"Perpetual Protocol","Symbol":"PERP"},{"Name":"Nervos Network","Symbol":"CKB"},{"Name":"Telcoin","Symbol":"TEL"},{"Name":"Synthetix","Symbol":"SNX"},{"Name":"SwissBorg","Symbol":"CHSB"},{"Name":"Storj","Symbol":"STORJ"},{"Name":"GateToken","Symbol":"GT"},{"Name":"Flux","Symbol":"FLUX"},{"Name":"Ontology","Symbol":"ONT"},{"Name":"UMA","Symbol":"UMA"},{"Name":"SKALE Network","Symbol":"SKL"},{"Name":"Celer Network","Symbol":"CELR"},{"Name":"Neutrino USD","Symbol":"USDN"},{"Name":"IOST","Symbol":"IOST"},{"Name":"Chromia","Symbol":"CHR"},{"Name":"Ocean Protocol","Symbol":"OCEAN"},{"Name":"Hive","Symbol":"HIVE"},{"Name":"dYdX","Symbol":"DYDX"},{"Name":"Ren","Symbol":"REN"},{"Name":"NuCypher","Symbol":"NU"},{"Name":"Polymath","Symbol":"POLY"},{"Name":"DigiByte","Symbol":"DGB"},{"Name":"Raydium","Symbol":"RAY"},{"Name":"Fei USD","Symbol":"FEI"},{"Name":"Golem","Symbol":"GLM"},{"Name":"Nano","Symbol":"XNO"},{"Name":"Serum","Symbol":"SRM"},{"Name":"JUST","Symbol":"JST"},{"Name":"WINkLink","Symbol":"WIN"},{"Name":"Dusk Network","Symbol":"DUSK"},{"Name":"Moonriver","Symbol":"MOVR"},{"Name":"CEEK VR","Symbol":"CEEK"},{"Name":"XYO","Symbol":"XYO"},{"Name":"OriginTrail","Symbol":"TRAC"},{"Name":"Dent","Symbol":"DENT"},{"Name":"Ultra","Symbol":"UOS"},{"Name":"Fetch.ai","Symbol":"FET"},{"Name":"Casper","Symbol":"CSPR"},{"Name":"Request","Symbol":"REQ"},{"Name":"WazirX","Symbol":"WRX"},{"Name":"Reserve Rights","Symbol":"RSR"},{"Name":"Keep3rV1","Symbol":"KP3R"},{"Name":"MyNeighborAlice","Symbol":"ALICE"},{"Name":"Swipe","Symbol":"SXP"},{"Name":"PAX Gold","Symbol":"PAXG"},{"Name":"Chrono.tech","Symbol":"TIME"},{"Name":"COTI","Symbol":"COTI"},{"Name":"Biconomy","Symbol":"BICO"},{"Name":"Phantasma","Symbol":"SOUL"},{"Name":"Function X","Symbol":"FX"},{"Name":"Injective","Symbol":"INJ"},{"Name":"Aragon","Symbol":"ANT"},{"Name":"Powerledger","Symbol":"POWR"},{"Name":"DigitalBits","Symbol":"XDB"},{"Name":"Cartesi","Symbol":"CTSI"},{"Name":"MediBloc","Symbol":"MED"},{"Name":"Lisk","Symbol":"LSK"},{"Name":"Mdex","Symbol":"MDX"},{"Name":"Dvision Network","Symbol":"DVI"},{"Name":"Alpha Finance Lab","Symbol":"ALPHA"},{"Name":"Reef","Symbol":"REEF"},{"Name":"Constellation","Symbol":"DAG"},{"Name":"VeThor Token","Symbol":"VTHO"},{"Name":"Energy Web Token","Symbol":"EWT"},{"Name":"Bitcoin Standard Hashrate Token","Symbol":"BTCST"},{"Name":"Conflux","Symbol":"CFX"},{"Name":"Verge","Symbol":"XVG"},{"Name":"Sun (New)","Symbol":"SUN"},{"Name":"aelf","Symbol":"ELF"},{"Name":"Ardor","Symbol":"ARDR"},{"Name":"Orchid","Symbol":"OXT"},{"Name":"Bitcoin Diamond","Symbol":"BCD"},{"Name":"Civic","Symbol":"CVC"},{"Name":"Status","Symbol":"SNT"},{"Name":"ASD","Symbol":"ASD"},{"Name":"iExec RLC","Symbol":"RLC"},{"Name":"MXC","Symbol":"MXC"},{"Name":"Divi","Symbol":"DIVI"},{"Name":"Origin Protocol","Symbol":"OGN"}]}
    #res = requests.get('https://alpha-kong-crypto.intellihub.ai/topcoins-list')
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
            #response = res.json()
            symbol = ""
            for item in res['cryptocurrencies']: 
                if item['Name'].lower() == coinname.lower():
                   symbol = item['Symbol']
            symbols.append(symbol)
            ids.append(artid)
            coins.append(coinname)
            links.append(link)
            desc.append(desnew)
            shortdesc.append(sd)
            titles.append(title)
            times.append(date)
        except Exception as e:
            print(e)
    
    data = {'ArticleID': ids, 'Coin': coins, 'Symbol': symbols, 'Title' : titles, 'Shortdescription' : shortdesc, 'Time' : times, 'Link' : links, 'Description' : desc}
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
    for i,artid,c,sym,t,sd,tim,l,d,tent,dent in df.itertuples():
            score = sid.polarity_scores(str(d))
            scores.append(score)

    df['scores'] = scores

    df['score'] = df['scores'].apply(lambda d:d['compound'])
    df['Overall_bias'] = df['score'].apply(lambda score: 'Positive' if score > 0.5 else 'Negative' if score < -0.5 else 'Neutral')
    df.drop('scores', axis = 1, inplace = True)
    
    oneword_list = []
    twoword_list = []
    threeword_list = []
    for i,artid,c,sym,t,sd,ti,l,d,te,de,s,b in df.itertuples():
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

