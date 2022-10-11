def get_predict_rub_salary(salary_from, salary_to):
    """Get expected salaries from vacancies"""
    if salary_from and salary_to:
        return (salary_from + salary_to) // 2
    elif salary_from:
        return int(salary_from * 1.2)
    elif salary_to:
        return int(salary_to * 0.8)


def get_avg_salary(salaries):
    """Get average salaries"""
    if len:
        avg_salary = round(sum(salaries) / len(salaries))
    else:
        return 0
    return avg_salary
