from pprint import pprint

import requests


def get_vacancies(language):
    """Getting vacancies from HeadHunter"""
    params = {
        'text': f'Программист {language}',
        'area': '1',
        'only_with_salary': 'true'
    }
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    response.raise_for_status()
    return response.json()['items']


def get_vacancies_count(language):
    popular_langs = {}
    params = {
        'text': language,
        'area': '1',
    }
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    response.raise_for_status()
    popular_langs[language] = response.json()['found']
    return popular_langs


def predict_rub_salary(vacancies):
    for salary in vacancies:
        if salary['salary']['currency'] != 'RUR':
            print(None)
        if salary['salary']['from'] and salary['salary']['to']:
            avg_salary = (salary['salary']['from'] + salary['salary']['to']) / 2
            print(int(avg_salary))
        elif salary['salary']['from']:
            from_avg_salary = salary['salary']['from'] * 1.2
            print(int(from_avg_salary))
        elif salary['salary']['to']:
            to_avg_salary = salary['salary']['to'] * 0.8
            print(int(to_avg_salary))


def get_salary():
    params = {
        'text': 'Python',
        'area': '1',
        'only_with_salary': 'true'
    }
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    response.raise_for_status()
    for i in response.json()['items']:
        pprint(i['salary'])


def main():
    languages = [
        'Python',
        'Java',
        'Javascript',
        'Ruby',
        'PHP',
        'C++',
        'C#',
        'C',
        'Scala',
        'Swift'
    ]
    for language in languages:
        predict_rub_salary(get_vacancies(language))


if __name__ == '__main__':
    main()
