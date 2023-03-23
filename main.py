import statistics
import requests
import json
import logging

from datetime import date
from database import *
from bs4 import BeautifulSoup

# настраиваем логирование

logging.getLogger('sqlalchemy').setLevel(logging.ERROR)
logging.basicConfig(filename='vacancies.log', level=logging.WARNING,
                    encoding="utf-8",
                    format='%(asctime)s - %(levelname)s - %(message)s')


def converter_usd():
    """конвертирование рублей в USD"""
    url_usd = "https://www.banki.ru/products/currency/usd/"
    response = requests.get(url_usd)
    soup = BeautifulSoup(response.content, 'html.parser')
    usd = soup.find('div', {'class': 'currency-table__large-text'}).text
    usd = float(usd.replace(",", "."))
    return usd


def get_found(session):
    """получение количества вакансий и подсчёт зарплаты"""
    url = "https://api.hh.ru/vacancies"
    # список вакансий, можно изменить при необходимости.
    params_list = ["python", "javascript", "c++", "C#", "java", "Go", "PHP",
                   "Kotlin", "Rust", "Ruby", "Swift", "TypeScript"]
    data_time = date.today()
    for param in params_list:
        try:
            params = {"text": param}
            response = requests.get(url, params=params)  # отправляем запрос
            response.raise_for_status()  # проверка нет ли ошибок в ответе
            data = json.loads(response.text)
            found = data["found"]
            vacancy_salary = []  # Вакансии с зп
            vacancy_not_salary = []  # Вакансии без зп
            vacancy_junior = []  # Вакансии джуна или начальные показатели
            vacancy_salaries = []

            for vacancy in data["items"]:
                try:
                    if "salary" in vacancy:
                        currency = vacancy["salary"]["currency"]  # USD или RUB
                        salary_from = vacancy["salary"]["from"]  # зп от
                        salary_to = vacancy["salary"]["to"]  # зп до
                        if salary_from is not None and salary_to is not None:
                            # Конвертируем валюту, если это не рубли
                            if currency != "RUR":
                                salary_from = salary_from * converter_usd()
                                salary_to = salary_to * converter_usd()
                            # добавляем в список с зп если два значения верны
                            vacancy_salary.append(vacancy)
                        elif salary_from and not salary_to:
                            if currency != "RUR":
                                salary_from = salary_from * converter_usd()
                            vacancy_junior.append(salary_from)
                        else:
                            # Если нет, то в отдельный список
                            vacancy_not_salary.append(vacancy)
                except TypeError:
                    logging.warning(
                        f"Ошибка при обработке вакансии {vacancy} in {param}")

            if len(vacancy_salary) > 0:

                # высчитываем среднюю зп из vacancy_salary
                for vacancy in vacancy_salary:
                    salary_from = vacancy["salary"]["from"]
                    salary_to = vacancy["salary"]["to"]
                    average_salary = (salary_from + salary_to) / 2
                    vacancy_salaries.append(average_salary)

            if len(vacancy_junior) > 0:
                junior_salaries = []
                for junior in vacancy_junior:
                    junior_salaries.append(junior)
                average_junior_salary = round(statistics.mean(junior_salaries),
                                              0)
                print(
                    f"Средняя зарплата джуниора по вакансии '{param}': {average_junior_salary:.0f}")

                average_salary = round(statistics.mean(vacancy_salaries), 0)
                print(
                    f"Средняя зарплата по вакансии '{param}': {average_salary:.0f}")
                # добавляем значения в базу данных
                vacancy = Vacancy(name=param, count=found,
                                  average_salary=average_salary,
                                  data_time=data_time,
                                  junior_salary=average_junior_salary)
                session.add(vacancy)
                session.commit()
        except (
                requests.exceptions.RequestException,
                json.JSONDecodeError) as e:
            logging.error(
                f"Не удалось получить данные о вакансиях для {param}: {e}")
            continue


if __name__ == '__main__':
    try:
        get_found(session)
    except Exception as e:
        print("Произошла ошибка:", e)
    finally:
        session.close()
