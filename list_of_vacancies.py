import os
from pprint import pprint
from dotenv import load_dotenv
import requests


# def get_vacancies_hh(language):
#     """Getting vacancies from HeadHunter"""
#     page = 0
#     pages_number = 1
#     vacancies = []
#     while page < pages_number:
#         params = {
#             'text': f'Программист {language}',
#             'area': '1',
#             'only_with_salary': 'true',
#             'page': page
#         }
#         response = requests.get('https://api.hh.ru/vacancies', params=params)
#         response.raise_for_status()
#         page += 1
#         pages_number += 1
#         if not response.json()['items']:
#             break
#         else:
#             vacancies.extend(response.json()['items'])
#     return vacancies


def get_vacancies_sj(secret_key, language):
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


def predict_rub_salary_sj(vacancy):
    predict_salaries = []
    for salary in vacancy:
        if salary['currency'] != 'rub':
            continue
        if salary['payment_from'] and salary['payment_to']:
            predict_salaries.append((salary['payment_from'] + salary['payment_to']) // 2)
        if salary['payment_from']:
            predict_salaries.append(int(salary['payment_from'] * 1.2))
        if salary['payment_to']:
            predict_salaries.append(int(salary['payment_to'] * 0.8))
    return predict_salaries


def get_vacancies_count_hh(language):
    params = {
        'text': f'Программист {language}',
        'area': '1',
    }
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    response.raise_for_status()
    return response.json()['found']


def get_vacancies_count_sj(secret_key, language):
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


# def predict_rub_salary(vacancies):
#     predict_salaries = []
#     for salary in vacancies:
#         if salary['salary']['currency'] != 'RUR':
#             continue
#         if salary['salary']['from'] and salary['salary']['to']:
#             predict_salaries.append((salary['salary']['from'] + salary['salary']['to']) // 2)
#         if salary['salary']['from']:
#             predict_salaries.append(int(salary['salary']['from'] * 1.2))
#         if salary['salary']['to']:
#             predict_salaries.append(int(salary['salary']['to'] * 0.8))
#     return predict_salaries


def get_avg_salary(salaries):
    avg_salary = round(sum(salaries) / len(salaries))
    return avg_salary


# def get_salary():
#     params = {
#         'text': 'Python',
#         'area': '1',
#         'only_with_salary': 'true'
#     }
#     response = requests.get('https://api.hh.ru/vacancies', params=params)
#     response.raise_for_status()
#     for i in response.json()['items']:
#         pprint(i['salary'])


def main():
    load_dotenv()
    secret_key = os.environ['SECRET_KEY']
    # a = get_vacancies_sj(secret_key)
    # print(predict_rub_salary_sj(a))
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
    dict_ = {}
    for language in languages:
        a = predict_rub_salary_sj(get_vacancies_sj(secret_key, language))
        dict_[language] = {'vacancies_found': get_vacancies_count_sj(secret_key, language),
                           'vacancies_processed': len(a),
                           "average_salary": get_avg_salary(a)}
    pprint(dict_)

    # dict_ = {}
    # for language in languages:
    #     a = predict_rub_salary(get_vacancies(language))
    #     dict_[language] = {'vacancies_found': get_vacancies_count(language),
    #                        'vacancies_processed': len(a),
    #                        "average_salary": get_avg_salary(a)}
    # pprint(dict_)


if __name__ == '__main__':
    main()
