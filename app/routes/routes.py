from calendar import day_abbr
from re import S
from turtle import pos
from fastapi import APIRouter,Request

from ..models.models import Article, inputData
from ..config.database import collection
import requests
import datetime

api_router = APIRouter()

def addreview(l1,l2,l3, doc):
        for r in doc['One_word_Reviews']:
            if r not in l1:
                l1.append(r)
        for r in doc['Two_word_Reviews']:
            l2.append(r)
        for r in doc['Three_word_Reviews']:
            l3.append(r)

# retrieve
@api_router.get("/")
async def root():
    return {"Hello" : "World"}

@api_router.get("/api/articles") # Get all articles
async def get_all_articles():
    articles = []
    cursor = collection.find({})
    for document in cursor:
        articles.append(Article(**document))
    return articles

@api_router.get("/api/articles/date/") # Get articles with coin name and date 
async def get_articles(request: Request):
    info = await request.json()
    date = info['date']
    article = []
    cursor = collection.find({})
    for document in cursor:
        if (document['Time'] == date):
            item = Article(**document)
            article.append(item)
    return article

@api_router.get("/api/articles/coin/") # Get articles with coin name and date 
async def get_articles(request: Request):
    info = await request.json()
    coin = info['coin']
    article = []
    cursor = collection.find({})
    for document in cursor:
        if (document['Coin'] == coin):
            item = Article(**document)
            article.append(item)
    return article

@api_router.get("/api/articles/datecoin/") # Get articles with coin name and date 
async def get_articles(request: Request):
    info = await request.json()
    coin = info['coin']
    date = info['date']
    article = []
    cursor = collection.find({})
    for document in cursor:
        if (document['Time'] == date) & (document['Coin'] == coin):
            item = Article(**document)
            article.append(item)
    return article

@api_router.post("/api/articles/sentiment/")
async def get_sentiment(data: inputData): # Gives the weekly sentiment of the provided coin  
    # Return overall sentiment, list of words for sentiment.
    res = {"cryptocurrencies":[{"Name":"Bitcoin","Symbol":"BTC"},{"Name":"Ethereum","Symbol":"ETH"},{"Name":"BNB","Symbol":"BNB"},{"Name":"Tether","Symbol":"USDT"},{"Name":"Cardano","Symbol":"ADA"},{"Name":"USD Coin","Symbol":"USDC"},{"Name":"Solana","Symbol":"SOL"},{"Name":"XRP","Symbol":"XRP"},{"Name":"Terra","Symbol":"LUNA"},{"Name":"Polkadot","Symbol":"DOT"},{"Name":"Dogecoin","Symbol":"DOGE"},{"Name":"Avalanche","Symbol":"AVAX"},{"Name":"Polygon","Symbol":"MATIC"},{"Name":"Shiba Inu","Symbol":"SHIB"},{"Name":"Binance USD","Symbol":"BUSD"},{"Name":"NEAR Protocol","Symbol":"NEAR"},{"Name":"Chainlink","Symbol":"LINK"},{"Name":"Crypto.com Coin","Symbol":"CRO"},{"Name":"Wrapped Bitcoin","Symbol":"WBTC"},{"Name":"TerraUSD","Symbol":"UST"},{"Name":"Uniswap","Symbol":"UNI"},{"Name":"Litecoin","Symbol":"LTC"},{"Name":"Dai","Symbol":"DAI"},{"Name":"Cosmos","Symbol":"ATOM"},{"Name":"Algorand","Symbol":"ALGO"},{"Name":"Fantom","Symbol":"FTM"},{"Name":"TRON","Symbol":"TRX"},{"Name":"Bitcoin Cash","Symbol":"BCH"},{"Name":"FTX Token","Symbol":"FTT"},{"Name":"Stellar","Symbol":"XLM"},{"Name":"Internet Computer","Symbol":"ICP"},{"Name":"Decentraland","Symbol":"MANA"},{"Name":"Hedera","Symbol":"HBAR"},{"Name":"Axie Infinity","Symbol":"AXS"},{"Name":"VeChain","Symbol":"VET"},{"Name":"Bitcoin BEP2","Symbol":"BTCB"},{"Name":"The Sandbox","Symbol":"SAND"},{"Name":"Filecoin","Symbol":"FIL"},{"Name":"Ethereum Classic","Symbol":"ETC"},{"Name":"Monero","Symbol":"XMR"},{"Name":"Theta Network","Symbol":"THETA"},{"Name":"Harmony","Symbol":"ONE"},{"Name":"Elrond","Symbol":"EGLD"},{"Name":"Tezos","Symbol":"XTZ"},{"Name":"Klaytn","Symbol":"KLAY"},{"Name":"UNUS SED LEO","Symbol":"LEO"},{"Name":"Helium","Symbol":"HNT"},{"Name":"Aave","Symbol":"AAVE"},{"Name":"IOTA","Symbol":"MIOTA"},{"Name":"PancakeSwap","Symbol":"CAKE"},{"Name":"EOS","Symbol":"EOS"},{"Name":"Stacks","Symbol":"STX"},{"Name":"The Graph","Symbol":"GRT"},{"Name":"BitTorrent","Symbol":"BTT"},{"Name":"Flow","Symbol":"FLOW"},{"Name":"Kusama","Symbol":"KSM"},{"Name":"Gala","Symbol":"GALA"},{"Name":"Curve DAO Token","Symbol":"CRV"},{"Name":"Maker","Symbol":"MKR"},{"Name":"Bitcoin SV","Symbol":"BSV"},{"Name":"Enjin Coin","Symbol":"ENJ"},{"Name":"THORChain","Symbol":"RUNE"},{"Name":"Quant","Symbol":"QNT"},{"Name":"eCash","Symbol":"XEC"},{"Name":"Zcash","Symbol":"ZEC"},{"Name":"Celo","Symbol":"CELO"},{"Name":"Oasis Network","Symbol":"ROSE"},{"Name":"Amp","Symbol":"AMP"},{"Name":"Neo","Symbol":"NEO"},{"Name":"KuCoin Token","Symbol":"KCS"},{"Name":"OKB","Symbol":"OKB"},{"Name":"Loopring","Symbol":"LRC"},{"Name":"Chiliz","Symbol":"CHZ"},{"Name":"Arweave","Symbol":"AR"},{"Name":"Basic Attention Token","Symbol":"BAT"},{"Name":"Huobi Token","Symbol":"HT"},{"Name":"Waves","Symbol":"WAVES"},{"Name":"TrueUSD","Symbol":"TUSD"},{"Name":"Dash","Symbol":"DASH"},{"Name":"Kadena","Symbol":"KDA"},{"Name":"Secret","Symbol":"SCRT"},{"Name":"Nexo","Symbol":"NEXO"},{"Name":"Mina","Symbol":"MINA"},{"Name":"yearn.finance","Symbol":"YFI"},{"Name":"Compound","Symbol":"COMP"},{"Name":"IoTeX","Symbol":"IOTX"},{"Name":"XDC Network","Symbol":"XDC"},{"Name":"Holo","Symbol":"HOT"},{"Name":"NEM","Symbol":"XEM"},{"Name":"1inch Network","Symbol":"1INCH"},{"Name":"Ravencoin","Symbol":"RVN"},{"Name":"Pax Dollar","Symbol":"USDP"},{"Name":"Theta Fuel","Symbol":"TFUEL"},{"Name":"Decred","Symbol":"DCR"},{"Name":"OMG Network","Symbol":"OMG"},{"Name":"SushiSwap","Symbol":"SUSHI"},{"Name":"Kava","Symbol":"KAVA"},{"Name":"Bancor","Symbol":"BNT"},{"Name":"BORA","Symbol":"BORA"},{"Name":"Zilliqa","Symbol":"ZIL"},{"Name":"Qtum","Symbol":"QTUM"},{"Name":"WAX","Symbol":"WAXP"},{"Name":"APENFT","Symbol":"NFT"},{"Name":"WOO Network","Symbol":"WOO"},{"Name":"Velas","Symbol":"VLX"},{"Name":"renBTC","Symbol":"RENBTC"},{"Name":"Celsius","Symbol":"CEL"},{"Name":"Ankr","Symbol":"ANKR"},{"Name":"Livepeer","Symbol":"LPT"},{"Name":"Syscoin","Symbol":"SYS"},{"Name":"Immutable X","Symbol":"IMX"},{"Name":"Audius","Symbol":"AUDIO"},{"Name":"Dogelon Mars","Symbol":"ELON"},{"Name":"Gnosis","Symbol":"GNO"},{"Name":"ICON","Symbol":"ICX"},{"Name":"Voyager Token","Symbol":"VGX"},{"Name":"Revain","Symbol":"REV"},{"Name":"Siacoin","Symbol":"SC"},{"Name":"Horizen","Symbol":"ZEN"},{"Name":"Bitcoin Gold","Symbol":"BTG"},{"Name":"0x","Symbol":"ZRX"},{"Name":"Perpetual Protocol","Symbol":"PERP"},{"Name":"Nervos Network","Symbol":"CKB"},{"Name":"Telcoin","Symbol":"TEL"},{"Name":"Synthetix","Symbol":"SNX"},{"Name":"SwissBorg","Symbol":"CHSB"},{"Name":"Storj","Symbol":"STORJ"},{"Name":"GateToken","Symbol":"GT"},{"Name":"Flux","Symbol":"FLUX"},{"Name":"Ontology","Symbol":"ONT"},{"Name":"UMA","Symbol":"UMA"},{"Name":"SKALE Network","Symbol":"SKL"},{"Name":"Celer Network","Symbol":"CELR"},{"Name":"Neutrino USD","Symbol":"USDN"},{"Name":"IOST","Symbol":"IOST"},{"Name":"Chromia","Symbol":"CHR"},{"Name":"Ocean Protocol","Symbol":"OCEAN"},{"Name":"Hive","Symbol":"HIVE"},{"Name":"dYdX","Symbol":"DYDX"},{"Name":"Ren","Symbol":"REN"},{"Name":"NuCypher","Symbol":"NU"},{"Name":"Polymath","Symbol":"POLY"},{"Name":"DigiByte","Symbol":"DGB"},{"Name":"Raydium","Symbol":"RAY"},{"Name":"Fei USD","Symbol":"FEI"},{"Name":"Golem","Symbol":"GLM"},{"Name":"Nano","Symbol":"XNO"},{"Name":"Serum","Symbol":"SRM"},{"Name":"JUST","Symbol":"JST"},{"Name":"WINkLink","Symbol":"WIN"},{"Name":"Dusk Network","Symbol":"DUSK"},{"Name":"Moonriver","Symbol":"MOVR"},{"Name":"CEEK VR","Symbol":"CEEK"},{"Name":"XYO","Symbol":"XYO"},{"Name":"OriginTrail","Symbol":"TRAC"},{"Name":"Dent","Symbol":"DENT"},{"Name":"Ultra","Symbol":"UOS"},{"Name":"Fetch.ai","Symbol":"FET"},{"Name":"Casper","Symbol":"CSPR"},{"Name":"Request","Symbol":"REQ"},{"Name":"WazirX","Symbol":"WRX"},{"Name":"Reserve Rights","Symbol":"RSR"},{"Name":"Keep3rV1","Symbol":"KP3R"},{"Name":"MyNeighborAlice","Symbol":"ALICE"},{"Name":"Swipe","Symbol":"SXP"},{"Name":"PAX Gold","Symbol":"PAXG"},{"Name":"Chrono.tech","Symbol":"TIME"},{"Name":"COTI","Symbol":"COTI"},{"Name":"Biconomy","Symbol":"BICO"},{"Name":"Phantasma","Symbol":"SOUL"},{"Name":"Function X","Symbol":"FX"},{"Name":"Injective","Symbol":"INJ"},{"Name":"Aragon","Symbol":"ANT"},{"Name":"Powerledger","Symbol":"POWR"},{"Name":"DigitalBits","Symbol":"XDB"},{"Name":"Cartesi","Symbol":"CTSI"},{"Name":"MediBloc","Symbol":"MED"},{"Name":"Lisk","Symbol":"LSK"},{"Name":"Mdex","Symbol":"MDX"},{"Name":"Dvision Network","Symbol":"DVI"},{"Name":"Alpha Finance Lab","Symbol":"ALPHA"},{"Name":"Reef","Symbol":"REEF"},{"Name":"Constellation","Symbol":"DAG"},{"Name":"VeThor Token","Symbol":"VTHO"},{"Name":"Energy Web Token","Symbol":"EWT"},{"Name":"Bitcoin Standard Hashrate Token","Symbol":"BTCST"},{"Name":"Conflux","Symbol":"CFX"},{"Name":"Verge","Symbol":"XVG"},{"Name":"Sun (New)","Symbol":"SUN"},{"Name":"aelf","Symbol":"ELF"},{"Name":"Ardor","Symbol":"ARDR"},{"Name":"Orchid","Symbol":"OXT"},{"Name":"Bitcoin Diamond","Symbol":"BCD"},{"Name":"Civic","Symbol":"CVC"},{"Name":"Status","Symbol":"SNT"},{"Name":"ASD","Symbol":"ASD"},{"Name":"iExec RLC","Symbol":"RLC"},{"Name":"MXC","Symbol":"MXC"},{"Name":"Divi","Symbol":"DIVI"},{"Name":"Origin Protocol","Symbol":"OGN"}]}
    # res = requests.get('https://alpha-kong-crypto.intellihub.ai/topcoins-list')
     #response = res.json()
    coin_fl = 0
    if data.coin != "":
        coin = data.coin.lower()
        coin_fl = 1
    else:
        coin = data.symbol
    reqdate = datetime.datetime.now() - datetime.timedelta(weeks = 4, days= 17)
    cursor = collection.find({})
    articles = []
    pos1word = []
    pos2word = []
    pos3word = []
    neg1word = []
    neg2word = []
    neg3word = []
    neu1word = []
    neu2word = []
    neu3word = []
    poscount = 0
    negcount = 0
    neucount = 0
    coinid = ''
    if coin_fl:
        coinid = 'Coin'
    else:
        coinid = 'Coin'
        for item in res['cryptocurrencies']: 
            if item['Symbol'].lower() == coin.lower():
                coin = item['Name'].lower()
    for doc in cursor:
        if (doc[coinid] == coin):
            strdate = doc['Time']
            date = datetime.datetime.strptime(strdate, '%Y-%m-%d')
            if date > reqdate:
                item = Article(**doc)
                if doc['score'] > 0.5:
                    addreview(pos1word, pos2word, pos3word, doc)
                    poscount = poscount+1
                elif doc['score'] < -0.5:
                    addreview(neg1word, neg2word, neg3word, doc)
                    negcount = negcount+1
                else:
                    addreview(neu1word, neu2word, neu3word, doc)
                    neucount = neucount+1
                articles.append(item)

    totalcount = len(articles) 

    if len(articles) == 0:
        return "No Articles Found"
    
    words = {
                "PositiveWords" : { 'Oneword': pos1word, "Twoword": pos2word, "Threeword": pos3word},
                "NegativeWords" : {"Oneword" : neg1word, "Twoword" : neg2word,"Threeword" : neg3word},
                "NeutralWords" : {"Oneword" : neu1word, "Twoword" : neu2word,"Threeword" : neu3word}
            }
    return {"Total": totalcount, "Positive" : poscount, "Negative" : negcount, "Neutral" : neucount, "Words" : words }

# async def get_todo(id: str):
#     return todos_serializer(collection_name.find_one({"_id": ObjectId(id)}))

