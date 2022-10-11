import os

import requests
from dotenv import load_dotenv
from terminaltables import AsciiTable

from average_salary import get_avg_salary


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
            'town': 4,
            'catalogues': 33,
            'keyword': f'Программист {language}',
            'no_agreement': 1,
            'page': page
        }
        response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=header, params=params)
        response.raise_for_status()
        page += 1
        pages_number += 1
        vacancies = response.json()['objects']
        if not vacancies:
            break
        else:
            list_of_vacancies.extend(vacancies)
        return list_of_vacancies


def get_vacancies_count_sj(secret_key, language):
    """Get vacancies count"""
    header = {
        'X-Api-App-Id': secret_key
    }
    params = {
        'town': 4,
        'catalogues': 33,
        'keyword': f'Программист {language}',
        'no_agreement': 1
    }
    response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=header, params=params)
    response.raise_for_status()
    return response.json()['total']


def predict_rub_salary_sj(vacancies):
    """Get predicted salaries from vacancies"""
    predict_salaries = []
    for salary in vacancies:
        if salary['currency'] != 'rub':
            continue
        if salary['payment_from'] and salary['payment_to']:
            predict_salaries.append((salary['payment_from'] + salary['payment_to']) // 2)
        if salary['payment_from']:
            predict_salaries.append(int(salary['payment_from'] * 1.2))
        if salary['payment_to']:
            predict_salaries.append(int(salary['payment_to'] * 0.8))
    return predict_salaries
