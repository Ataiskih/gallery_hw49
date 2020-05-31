from sqlalchemy import create_engine, \
    Column, Integer, String, Text, ForeignKey       # связь с базой и инструмент для созд параметров колон в табл
from sqlalchemy.orm import relationship     # инструмент для созд связи меджу колоннами др табл
from sqlalchemy.orm.session import sessionmaker     # инструмент созд сессии
from sqlalchemy.ext.declarative import declarative_base     # класс-образец

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/gallery_db"
)
# ("какая программа://логин:пароль@localhost:номер порта [по умолч 5432]/имя базы данных")
Base = declarative_base()       # класс-образец от sqlalchemy.ext.declarative

class Author(Base):     # происываем DML команды (колонны и парараметры)
    __tablename__ = 'author'    # создание таблицы 'author' в postgres
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    country = Column(String(255))
    picture = relationship("Picture")       # обрантая связь (получение данных с ) с табл picture

    def __str__(self):      # функция отображения 
        self.name


class Picture(Base):     # происываем DML команды (колонны и парараметры)
    __tablename__ = 'picture'    # создание таблицы 'picture' в postgres
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    url = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, default=0)
    author = Column(ForeignKey("author.id"))

    def __str__(self):         # функция отображения 
        self.name

Base.metadata.create_all(engine)    # создание баз в таблице

session = sessionmaker(engine)()       # применение записей в sql
