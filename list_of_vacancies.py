from pprint import pprint

import requests


def get_vacancies():
    """Getting vacancies from HeadHunter"""
    vacancies = []
    params = {
        'text': 'Программист',
        'area': '1',
        'only_with_salary': 'true'
    }
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    response.raise_for_status()
    for vacancy in response.json()['items']:
        vacancies.append(vacancy)
    return vacancies


def get_vacancies_count():
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
    popular_langs = {}
    for language in languages:
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
            print(avg_salary)
        elif salary['salary']['from']:
            from_avg_salary = salary['salary']['from'] * 1.2
            print(from_avg_salary)
        elif salary['salary']['to']:
            to_avg_salary = salary['salary']['to'] * 0.8
            print(to_avg_salary)
            # pprint(salary['salary'])
    # print(vacancies[0]['salary'])

def get_salary():
    params = {
        'text': 'Python',
        'area': '1',
        'salary': '100000',
        'only_with_salary': 'true'
    }
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    response.raise_for_status()
    for i in response.json()['items']:
        return i['salary']


def main():
    predict_rub_salary(get_vacancies())
    # pprint(get_vacancies())
    # pprint(get_vacancies_count())
    # pprint(get_salary())


if __name__ == '__main__':
    main()
