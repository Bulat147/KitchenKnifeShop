
from flask import Flask, render_template, request, make_response, session

from database.db_util import Database

def page_not_found(e):
    return render_template("error.html")

app = Flask(__name__)
app.secret_key = "777"
app.register_error_handler(404, page_not_found)

db = Database()



@app.route("/")
def knifes_list():

    knife_type = request.args.get("type")
    company = request.args.get("company")
    price = request.args.get("cool")

    type_search = ""
    company_search = ""
    price_search = ""
    where = ""
    ands = "AND"
    if knife_type is not None:
        type_search = "k.type=" + knife_type + ""


    if company is not None:
        pass

    if price is not None and price != 0:
        pass

    knifes = db.select("SELECT * FROM knife k"+ where + type_search +";")

    context = {
        'knifes': knifes,
        'title': "Главная",

    }

    return render_template("home_page.html", **context)


@app.route("/film/<int:film_id>")
def get_film(film_id):
    # переписываем запрос с помощью SQLAlchemy
    # в данном случае при отсутствии указанного фильма, выходит 404 ошибка
    film = db.get_or_404(Films, film_id)
    return render_template("film.html", title=film.name, film=film)


# метод для создания заметки
@app.route("/add_note", methods=['get', 'post'])
def add_note():
    if request.method == "POST":
        note = request.form.get('note')

        db.cur.execute("INSERT INTO notes(note) VALUES (%s)", (note, ))
        db.con.commit()
        return "Note was added"

    return render_template("note.html")



if __name__ == '__main__':
    app.run(port=8000, debug=True)