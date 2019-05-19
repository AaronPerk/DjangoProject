import requests
import random

def get_meme_options():
    url = 'https://memegen.link/api/templates/'
    #params = {'year': year, 'author': author}
    r = requests.get(url)

    result = r.json()
    options = []

    for key in result.keys():
        options.append((result[key][(result[key].rfind('/')+1):], key))

    return options

  
def randomMemeQuote(quote,meme):
    #Pass an array of quotes and an array of memes
    return random.choice(quote),random.choice(meme)


def getTrumpQuotes():
    
    trumpQuotes = []
    #Generate 20 random Trump Quotes
    for i in range(20):
        
        url = 'https://api.tronalddump.io/random/quote'
        r = requests.get(url).json()['value']
        trumpQuotes.append(r)
        
    return trumpQuotes
