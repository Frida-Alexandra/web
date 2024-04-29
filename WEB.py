import requests
import json
import bs4
from fake_headers import Headers

def get_fake_headers():
    return Headers(browser="chrome", os="win").generate()

# Cписок вакансий
def search():
    response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2',
                        headers=get_fake_headers())
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    vacancies = soup.findAll('div', class_='vacancy-serp-item-body')
    parsed_data = []

    for vacancy in vacancies:
        link = vacancy.find('a', class_='bloko-link').get('href')
        position = vacancy.find('a', class_='bloko-link').text
        try:
            salary = vacancy.find('span', class_='bloko-header-section-2').text.replace("\u202f", " ").replace("\xa0", " ")
        except:
            salary = 'нет информации о ЗП'
        company_name = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace("\xa0", " ")
        location = vacancy.findAll('div', class_='bloko-text')[1].text.replace("\xa0", " ")

        parsed_data.append([link, position, salary, company_name, location])
   
    return parsed_data

# Cписок в словарь
def convert_to_dict(parsed_data):
    return [dict(zip(['link', 'position', 'salary', 'company_name', 'location'], row)) for row in parsed_data]

def write_json(parsed_data):
    with open('vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(parsed_data, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    search()
    write_json(convert_to_dict(search()))

