import requests
from bs4 import BeautifulSoup

PARAGRAPH_PER_VALUE = 1


def get_wiki_data(value):
    url = f'https://he.wikipedia.org/wiki/{value}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # remove all the tables because there are unnecessary p tags inside them
    for table in soup.find_all('table'):
        table.extract()

    # remove these small links [1], [2]...
    for sup in soup.find_all('sup'):
        sup.extract()

    paragraphs = soup.find_all('p')
    paragraphs = [p.get_text().strip() for p in paragraphs]
    print(paragraphs)
    for p in paragraphs:
        if p == 'אין בוויקיפדיה ערך בשם זה.':
            return []
    return paragraphs


def main():
    all_values_data = []
    with open('values_list.txt', 'r', encoding='utf-8') as file:
        for value in file.read().split('\n'):
            if value != '':
                paragraphs = get_wiki_data(value)
                if paragraphs:
                    all_values_data.append(paragraphs)

    with open('summary.txt', 'w', encoding='utf-8') as file:
        for value_data in all_values_data:
            for i in range(PARAGRAPH_PER_VALUE):
                file.write(value_data[i] + '\n')
            file.write('\n')


if __name__ == '__main__':
    main()
