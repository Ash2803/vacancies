import os

from dotenv import load_dotenv
from terminaltables import AsciiTable

from average_salary import get_avg_salary
from hh_vacancies import get_vacancies_hh, get_vacancies_count_hh, get_salaries_hh
from superjob_vacancies import get_vacancies_sj, get_vacancies_count_sj, get_salaries_sj


def create_table(jobs_stats, resource):
    """Creating table with vacancies stats"""
    title = resource
    statistics_table = [
        ['Язык программирования',
         'Вакансий найдено',
         'Вакансий обработано',
         'Средняя зарплата'],
    ]
    for language, stats in jobs_stats.items():
        statistics_table.append([language, stats['vacancies_found'],
                                 stats['vacancies_processed'],
                                 stats['average_salary']]
                                )
    table_instance = AsciiTable(statistics_table, title)
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
    load_dotenv()
    secret_key = os.environ['SJ_SECRET_KEY']
    sj_table_title = 'SuperJob Moscow'
    hh_table_title = 'HeadHunter Moscow'
    hh_jobs_stats = {}
    sj_jobs_stats = {}
    for language in languages:
        vacancies_hh = get_vacancies_hh(language)
        vacancies_sj = get_vacancies_sj(secret_key, language)
        hh_predicted_salary = get_salaries_hh(vacancies_hh)
        sj_predicted_salary = get_salaries_sj(vacancies_sj)
        hh_jobs_stats[language] = {'vacancies_found': get_vacancies_count_hh(vacancies_hh),
                                   'vacancies_processed': len(hh_predicted_salary),
                                   "average_salary": get_avg_salary(hh_predicted_salary)
                                   }
        sj_jobs_stats[language] = {'vacancies_found': get_vacancies_count_sj(vacancies_sj),
                                   'vacancies_processed': len(sj_predicted_salary),
                                   "average_salary": get_avg_salary(sj_predicted_salary)
                                   }
    print(create_table(hh_jobs_stats, hh_table_title))
    print(create_table(sj_jobs_stats, sj_table_title))


if __name__ == '__main__':
    main()
