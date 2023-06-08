import string
import random
from src.model import Short, Url
from flask_login import current_user

def save_url(link, alias=''):
    if not alias:
        alias = generate_alias()

    url = Url.get_by_link(link)
    if not url:
        url = Url(link=link)
        url.save()

    short_url = Short(alias=alias, url_id=url.id, owner_id=current_user.get_id())
    short_url.save()
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