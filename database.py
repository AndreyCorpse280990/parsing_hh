from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# Создаем соединение с базой данных
engine = create_engine('sqlite:///vacancies.db', echo=True)

# Создаем базовый класс
Base = declarative_base()

# Определяем модель таблицы vacancies
class Vacancy(Base):
    __tablename__ = 'vacancies'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    count = Column(Integer, nullable=False)
    data_time = Column(String(50), nullable=False)
    average_salary = Column(Integer, nullable=False)
    junior_salary = Column(Integer, nullable=False)

# Создаем таблицу в базе данных
Base.metadata.create_all(engine)

# Создаем сессию для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()
