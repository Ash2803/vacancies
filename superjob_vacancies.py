import os

import requests
from dotenv import load_dotenv

from average_salary import get_predict_rub_salary

TOWN = 4
CATALOGUE = 33
NO_AGREEMENT = 1


def get_vacancies_sj(secret_key, language):
    """Get vacancies from SuperJob"""
    page = 0
    pages_number = 1
    header = {
        'X-Api-App-Id': secret_key
    }
    list_of_vacancies = []
    while page < pages_number:
        params = {
            'town': TOWN,
            'catalogues': CATALOGUE,
            'keyword': f'Программист {language}',
            'no_agreement': NO_AGREEMENT,
            'page': page
        }
        response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=header, params=params)
        response.raise_for_status()
        page += 1
        pages_number += 1
        vacancies = response.json()
        if not vacancies:
            break
        else:
            return vacancies


def get_vacancies_count_sj(vacancies):
    """Get vacancies count"""
    return vacancies['total']


def get_salaries_sj(vacancy):
    """Get salaries from vacancies"""
    predicted_salaries = []
    for vacancy_salary in vacancy['objects']:
        if vacancy_salary['currency'] != 'rub':
            continue
        salary_from = vacancy_salary['payment_from']
        salary_to = vacancy_salary['payment_to']
        predicted_salary = get_predict_rub_salary(salary_from, salary_to)
        predicted_salaries.append(predicted_salary)
    return predicted_salaries
