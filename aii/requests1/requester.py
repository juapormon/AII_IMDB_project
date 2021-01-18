from itertools import zip_longest

import requests
from models.news import News


def request():
    try:
        response = requests.get('https://sevilla.abc.es/rss/feeds/Sevilla_Sevilla.xml')
        response.raise_for_status()
    except requests.HTTPError as http_err:
        print(http_err)
    except Exception as err:
        print(err)
    else:
        return response.content


# https://docs.python.org/3/library/itertools.html#itertools-recipes
def grouper(iterable, n, fill_value=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fill_value)


def treatment(response_content):
    to_treat = response_content.decode().split('\n')
    targets = ['<pubDate>', '<link>', '<title>', '<description>']
    treated = []
    for text in to_treat:
        for tag in targets:
            if tag in text:
                treated.append(text)
                # treated.append(re.sub("<.*?>", "", text))
    return list(grouper(treated, 4))


def builder(treated):
    built = []
    for item in treated:
        built.append(News(item))
    return built


def main():
    req = request()
    treated = treatment(req)
    built = builder(treated)
    print(built)


if __name__ == '__main__':
    main()
