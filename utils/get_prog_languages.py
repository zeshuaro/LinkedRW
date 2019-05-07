import requests

from bs4 import BeautifulSoup


def main():
    url = 'https://en.wikipedia.org/wiki/List_of_programming_languages'
    r = requests.get(url)
    languages = []

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        divs = soup.find_all('div', {'class': 'div-col columns column-width'})

        for div in divs:
            languages += [x.text.lower() for x in div.find_all('li')]

    with open('prog_languages.txt', 'w') as f:
        f.write('\n'.join(languages))


if __name__ == '__main__':
    main()