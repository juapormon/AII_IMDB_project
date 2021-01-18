import requests
from bs4 import BeautifulSoup
import re

base_url = 'https://www.elseptimoarte.net'


def request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.HTTPError as http_err:
        print(http_err)
    except Exception as err:
        print(err)
    else:
        return response.content


def get_links(doc):
    soup = BeautifulSoup(doc, 'html.parser')
    content_list = soup.find('ul', class_='elements')
    links = [base_url + link['href'] for link in content_list.find_all('a')]
    return links


def get_pages(doc):
    soup = BeautifulSoup(doc, 'html.parser')
    return [base_url + a['href'] for a in soup.find('div', id='paginacion').find_all('a')]


def get_film_info(link):
    film_page = request(link)
    soup = BeautifulSoup(film_page, 'html.parser')
    categorias = [a.string for a in soup.find('p', class_='categorias').find_all('a')]
    ficha = soup.find('dl').find_all('dd')
    titulo = ficha[0].string.__str__()
    titulo_original = ficha[1].string.__str__()
    pais = ficha[2].a.string.__str__()
    estreno_espanya = ficha[3].string.__str__()
    director = soup.find('a', href=re.compile('^/directores/')).string.__str__()
    film = {
        'TITLE': titulo,
        'ORIGINAL_TITLE': titulo_original,
        'COUNTRIES': pais,
        'RELEASE_DATE': estreno_espanya,
        'DIRECTOR': director,
        'GENRES': ''.join(map(str, categorias))
    }
    return film


def main():
    req = request(base_url+'/estrenos/')
    films = []
    for link in get_links(req):
        films.append(
            get_film_info(link)
        )
    return films


# if __name__ == '__main__':
#     main()
