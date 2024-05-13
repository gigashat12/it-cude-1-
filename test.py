from bs4 import BeautifulSoup
import requests
from fuzzywuzzy import fuzz

user_request = input()
count = 0

for numder in range(1, 501):
    url = f'https://w140.zona.plus/movies/filter/sort-date?page={numder}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

#    https = 'https://w140.zona.plus/'+soup.find('li', class_='results-item-wrap').find('a', class_='results-item').get('href')

#    name = soup.find('li', class_='results-item-wrap').find('a', class_='results-item').get('title')

    films = soup.findAll('li', class_='results-item-wrap')

    data = []

    for film in films:

        https = 'https://w140.zona.plus/' + film.find('a', class_='results-item').get('href')
        name = film.find('a', class_='results-item').get('title')

        if fuzz.partial_ratio(user_request, name) >= 80:
            r_2 = requests.get(https)
            soup_2 = BeautifulSoup(r_2.text, 'lxml')
            text_1 = soup_2.find('div', class_='entity-desc-description').text
#            genre_1 = soup_2.find('a', class_='entity-desc-link').findall('span', class_='entity-desc-link-u')
#            time = soup_2.find("time datetime")
            data.append(name)
            data.append(text_1)
            data.append(https)
            count += 1

        if count >= 5:
            break
    for i in data:
        print(data[i])

#    grade = soup.find('li', class_='results-item-wrap').find('span', class_='results-item-rating').text
#    print(grade)
