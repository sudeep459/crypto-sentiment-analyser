
from pydantic import BaseModel
from typing import List

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
    One_word_Reviews: List[tuple]
    Two_word_Reviews: List[tuple]
    Three_word_Reviews: List[tuple]

