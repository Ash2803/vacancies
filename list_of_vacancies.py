from pprint import pprint

import requests


def get_vacancies(language):
    """Getting vacancies from HeadHunter"""
    page = 0
    pages_number = 1
    params = {
        'text': f'Программист {language}',
        'area': '1',
        'only_with_salary': 'true',
        'page': page
    }
    while page < pages_number:
        response = requests.get('https://api.hh.ru/vacancies', params=params)
        response.raise_for_status()
        page += 1
        return response.json()['items']


def get_vacancies_count(language):
    params = {
        'text': language,
        'area': '1',
    }
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    response.raise_for_status()
    return response.json()['found']


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
    return avg_salary


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
    dict_ = {}
    for language in languages:
        a = predict_rub_salary(get_vacancies(language))
        dict_[language] = {'vacancies_found': get_vacancies_count(language),
                           'vacancies_processed': len(a),
                           "average_salary": get_avg_salary(a)}
    pprint(dict_)


if __name__ == '__main__':
    main()
