import requests
from terminaltables import AsciiTable

from average_salary import get_avg_salary


def get_vacancies_hh(language):
    """Getting vacancies from HeadHunter"""
    page = 0
    pages_number = 1
    vacancies = []
    while page < pages_number:
        params = {
            'text': f'Программист {language}',
            'area': '1',
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


def create_table(jobs_stats):
    """Creating table with vacancies stats"""
    title = 'HeadHunter Moscow'
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
        predicted_salary = predict_rub_salary_hh(get_vacancies_hh(language))
        jobs_stats[language] = {'vacancies_found': get_vacancies_count_hh(language),
                                'vacancies_processed': len(predicted_salary),
                                "average_salary": get_avg_salary(predicted_salary)
                                }
    print(create_table(jobs_stats))


if __name__ == '__main__':
    main()
