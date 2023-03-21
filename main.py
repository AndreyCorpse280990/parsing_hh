import requests
import json

from datetime import date
from database import *


data_time = date.today()


def get_found():
    url = "https://api.hh.ru/vacancies"
    # Создаем список с несколькими значениями параметра поиска
    params_list = ["python", "javascript", "c++", "C#", "java", "Go", "PHP",
                   "Kotlin", "Rust", "Ruby", "Swift", "TypeScript"]

    for param in params_list:
        # Создаем словарь с параметрами поиска
        params = {"text": param}
        # Отправляем GET-запрос с параметрами поиска на сервер
        response = requests.get(url, params=params)
        # Парсим JSON-данные, полученные с сайта hh.ru
        data = json.loads(response.text)
        # Получаем значение found
        found = data["found"]
        print(data)
        # Выводим количество найденных вакансий на экран
        print(f"Найдено вакансий по запросу '{param}': {found} в {data_time}")
        vacancy = Vacancy(name=param, count=found, data_time=data_time)
        session.add(vacancy)
        session.commit()


if __name__ == '__main__':
    get_found()
