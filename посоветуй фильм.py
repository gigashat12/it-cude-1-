
url = 'https://www.kinopoisk.ru/lists/movies/hd-must-see/?utm_referrer=www.google.com'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')
films = soup.findAll('li', class_='results-item-wrap')

data = []
for film in films:
        https = 'https://w140.zona.plus/' + film.find('a', class_='results-item').get('href')
        name = film.find('a', class_='results-item').get('title')
