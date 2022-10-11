import requests

from average_salary import get_predict_rub_salary


def get_vacancies_hh(language):
    """Getting vacancies from HeadHunter"""
    page = 0
    pages_number = 1
    city = 1
    list_of_vacancies = []
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
        vacancies = response.json()['items']
        if not vacancies:
            break
        else:
            list_of_vacancies.extend(vacancies)
    return list_of_vacancies


def get_vacancies_count_hh(language):
    """Get vacancies count"""
    params = {
        'text': f'Программист {language}',
        'area': '1',
    }
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    response.raise_for_status()
    return response.json()['found']


def get_salaries_hh(vacancy):
    """Get salaries from vacancies"""
    predicted_salaries = []
    for vacancy_salary in vacancy:
        if vacancy_salary['salary']['currency'] != 'RUR':
            continue
        salary_from = vacancy_salary['salary']['from']
        salary_to = vacancy_salary['salary']['to']
        predicted_salary = get_predict_rub_salary(salary_from, salary_to)
        predicted_salaries.append(predicted_salary)
    return predicted_salaries
