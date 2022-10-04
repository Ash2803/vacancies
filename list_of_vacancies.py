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
    predict_salaries = []
    for salary in vacancies:
        if salary['salary']['currency'] != 'RUR':
            continue
        if salary['salary']['from'] and salary['salary']['to']:
            predict_salaries.append((salary['salary']['from'] + salary['salary']['to']) // 2)
        if salary['salary']['from']:
            predict_salaries.append(int(salary['salary']['from'] * 1.2))
        if salary['salary']['to']:
            predict_salaries.append(int(salary['salary']['to'] * 0.8))
    return predict_salaries


def get_avg_salary(salaries):
    avg_salary = round(sum(salaries) / len(salaries))
    proceed = len(salaries)
    return avg_salary, proceed


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
        a = predict_rub_salary(get_vacancies(language))
        print(get_avg_salary(a))
        print(get_vacancies_count(language))


if __name__ == '__main__':
    main()
