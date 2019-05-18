import requests

def get_meme_options():
    url = 'https://memegen.link/api/templates/'
    #params = {'year': year, 'author': author}
    r = requests.get(url)

    result = r.json()
    options = []

    for key in result.keys():
        options.append((result[key][(result[key].rfind('/')+1):], key))

    return options