import string
import random
from src.model import Short

def save_url(url, customUrl=''):
    alias = customUrl
    if not customUrl:
        alias = generate_alias()

    print(url, 'its the url')
    short_url = Short(alias=alias, url=url)
    Short.save(short_url)
    return short_url
    



def generate_alias():
    characters = string.ascii_letters
    alias = ''
    while True:
        alias = ''.join(random.choices(characters, k=6))
        short_url = Short.get_by_alias(alias=alias)
        if not short_url:
            break
    return alias