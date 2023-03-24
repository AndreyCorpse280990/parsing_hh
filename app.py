from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database import Vacancy, Session, engine


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stats')
def stats():
    session = Session()
    vacancies = session.query(Vacancy).all()
    # здесь можно производить необходимые расчеты статистики и передавать результат в шаблон
    return render_template('stats.html', vacancies=vacancies)


if __name__ == '__main__':
    app.run(debug=True)


