import requests


def get_vacancies_hh(language):
    """Getting vacancies from HeadHunter"""
    page = 0
    pages_number = 1
    city = 1
    vacancies = []
    while page < pages_number:
        params = {
            'text': f'Программист {language}',
            'area': city,
            'only_with_salary': 'true',
            'page': page
        }
        response = requests.get('https://api.hh.ru/vacancies', params=params)
        response.raise_for_status()
        page += 1
        pages_number += 1
        if not response.json()['items']:
            break
        else:
            vacancies.extend(response.json()['items'])
    return vacancies


def get_vacancies_count_hh(language):
    """Get vacancies count"""
    params = {
        'text': f'Программист {language}',
        'area': '1',
    }
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    response.raise_for_status()
    return response.json()['found']


def predict_rub_salary_hh(vacancies):
    """Get predicted salaries from vacancies"""
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
