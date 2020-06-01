from flask import Flask, render_template, request
from database import *


app = Flask(__name__)
@app.route("/", methods = ["GET", "POST"])
@app.route("/<string:user_name>", methods = ["GET", "POST"])
def index(user_name = ""):
    if request.method == "GET":
        images = session.query(Picture).all()       # получение списка картин
    elif request.method == "POST":      # поиск
        search_key = request.form.get("search_key")     # получение с формы
        images = session.query(Picture).\
            filter(Picture.name.like("%{}%".format(search_key))).all()
    return render_template("index.html", images = images, user_name = user_name)

@app.route("/add")
def add():
    authors = session.query(Author)     # получение списка всех авторов 
    session.commit()        # конец сессии
    return render_template("form.html", authors=authors)    # передали в форму

@app.route("/reciever", methods=["POST"])
def reciever():
    url = request.form.get("url")     # данные из form.html
    name = request.form.get("name")     # данные из form.html
    description = request.form.get("description")     # данные из form.html
    price = int(request.form.get("price"))     # данные из form.html
    author = request.form.get("author")     # данные из form.html
    if author:      # проверка на пустоту
        author = int(author)
    
    new_image = Picture(
        name=name,
        url=url,
        description=description,
        price=price,
        author=author  
    )       # данные для записи в sql

    session.add(new_image)      # добавление записей картин в sql
    session.commit()        # конец сессии
    message = "Ваша картина  была добавлена успешно"   # добавление сообщения на стр susses 
    return render_template("success.html", message=message)

@app.route("/author_reciever", methods=["GET", "POST"])
def author_reciever():
    if request.method == "POST":
        name = request.form.get("name")     # данные из author_form.html
        country = request.form.get("country")     # данные из author_form.html
        new_author = Author(
            name=name,
            country=country
        )       # данные для записи в sql

        session.add(new_author)     # добавление записей новых авторов в sql
        session.commit()        # конец сессии
        message = "Автор был добавлен успешно"   # добавление сообщения на стр susses
        return render_template("success.html", message=message)
    
    elif request.method == "GET":
        return render_template("author_form.html")

@app.route("/details/<int:id>", methods = ["GET", "POST"])
def details(id):        # отображение записей более подробно на стр details.html
    if request.method == "GET":
        image = session.execute('''
            SELECT p.name, a.name AS author, p.price, p.description, p.url
            FROM Picture AS p
            JOIN Author AS a
            ON p.author = a.id
            WHERE p.id=%d
        ''' % id).first()
        session.commit()        # конец сессии
        return render_template("details.html", image = image)

    elif request.method == "POST":  
        image = session.query(Picture).filter_by(id=id).first()
        session.delete(image)
        session.commit()        # конец сессии
        message = "Вы успешно удалили запись"   # добавление сообщения на стр susses 
        return render_template("success.html", image = image, message=message)
    