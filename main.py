import statistics
import requests
import json

from datetime import date
from database import *


def get_found():
    url = "https://api.hh.ru/vacancies"
    params_list = ["python", "javascript", "c++", "C#", "java", "Go", "PHP",
                   "Kotlin", "Rust", "Ruby", "Swift", "TypeScript"]
    data_time = date.today()
    for param in params_list:
        params = {"text": param}
        response = requests.get(url, params=params)
        data = json.loads(response.text)
        found = data["found"]
        vacancy_salary = []
        vacancy_not_salary = []

        for vacancy in data["items"]:
            try:
                if "salary" in vacancy:
                    salary_from = vacancy["salary"]["from"]
                    salary_to = vacancy["salary"]["to"]
                    if salary_from is not None and salary_to is not None:
                        vacancy_salary.append(vacancy)
                    else:
                        vacancy_not_salary.append(vacancy)
            except TypeError:
                pass

        if len(vacancy_salary) > 0:
            vacancy_salaries = []
            for vacancy in vacancy_salary:
                salary_from = vacancy["salary"]["from"]
                salary_to = vacancy["salary"]["to"]
                average_salary = (salary_from + salary_to) / 2
                vacancy_salaries.append(average_salary)

            average_salary = round(statistics.mean(vacancy_salaries), 0)
            print(f"Средняя запрлата по вакансии '{param}': {average_salary:.0f}")

            vacancy = Vacancy(name=param, count=found, average_salary=average_salary, data_time=data_time)
            session.add(vacancy)
            session.commit()

if __name__ == '__main__':
    get_found()
