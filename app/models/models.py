
from pydantic import BaseModel
from typing import Dict, List, Optional

from typer import Option

class Article(BaseModel):
    Coin: str
    Title: str
    Shortdescription: str
    Time: str
    Link: str
    Description:str
    Title_Ents: List[str]
    Description_Ents: List[str]
    score: float
    Overall_bias: str
    One_word_Reviews: List[Dict]
    Two_word_Reviews: List[Dict]
    Three_word_Reviews: List[Dict]

class inputData(BaseModel):
    coin: str
    symbol: str

