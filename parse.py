from bs4 import BeautifulSoup, Comment
from urllib import urlopen


webpage = BeautifulSoup(urlopen('https://www.basketball-reference.com/teams/ATL/2017.html').read(), 'html.parser')


comment_arr = []
for comments in webpage.findAll(text=lambda text:isinstance(text, Comment)):
    content = comments.extract()
    if 'id=\"per_minute\"' in content:
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.findAll('table', {'id':'per_minute'})
