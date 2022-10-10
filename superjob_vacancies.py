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
    vacancies = []
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
        if not response.json()['objects']:
            break
        else:
            vacancies.extend(response.json()['objects'])
        return vacancies


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


def create_table(jobs_stats):
    """Creating table with vacancies stats"""
    title = 'SuperJob Moscow'
    table_data = [
        ['Язык программирования',
         'Вакансий найдено',
         'Вакансий обработано',
         'Средняя зарплата'],
    ]
    for key, value in jobs_stats.items():
        table_data.append([key, value['vacancies_found'],
                           value['vacancies_processed'],
                           value['average_salary']]
                          )
    table_instance = AsciiTable(table_data, title)
    return table_instance.table


def main():
    load_dotenv()
    secret_key = os.environ['SECRET_KEY']
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
    jobs_stats = {}
    for language in languages:
        predicted_salary = predict_rub_salary_sj(get_vacancies_sj(secret_key, language))
        jobs_stats[language] = {'vacancies_found': len(predicted_salary),
                                'vacancies_processed': get_vacancies_count_sj(secret_key, language),
                                "average_salary": get_avg_salary(predicted_salary)
                                }
    print(create_table(jobs_stats))


if __name__ == '__main__':
    main()
