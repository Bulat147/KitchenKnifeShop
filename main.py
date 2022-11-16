from flask import Flask, render_template, request, make_response, session, redirect, url_for

from database.db_util import Database


def page_not_found(e):
    return render_template("error.html")


app = Flask(__name__)
app.secret_key = "777"
app.register_error_handler(404, page_not_found)

db = Database()


@app.route('/check_pasw_login', methods=["POST"])
def check_password_login():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        psw_in_db = db.select(f"SELECT password from person p where p.login = '{login}'")
        if len(psw_in_db) == 0:
            return {"state": "none"}
        if password == psw_in_db[0]["password"]:
            return {"state": "true"}
        else:
            return {"state": "false"}


@app.route('/check_login_in_db', methods=["POST"])
def check_login_in_db():
    if request.method == "POST":
        login = request.form.get("login")
        persons = db.select(f"SELECT * FROM person WHERE login = '{login}'")
        if len(persons) > 0:
            return {"pers": "in"}
        else:
            return {"pers": "not"}


@app.route("/authorization")
def auth():
    context = {
        "title": "Авторизация"
    }
    return render_template("authorization.html", **context)


@app.route("/registration")
def registration():
    context = {
        "title": "Регистрация"

    }
    return render_template("registration.html", **context)


@app.route("/home", methods=['GET', 'POST'])
def knifes_list():
    if request.args.get("exit") == "on":
        session.pop("user_login", None)
    if request.method == 'POST':
        if request.form.get("registration") == "Регистрация":
            return redirect("/registration", 301)
        login = request.form.get("login")
        password = request.form.get("password")
        address = request.form.get("address")
        if address != "" and address is not None and login != "" and password != "":
            db.insert(f"INSERT INTO person VALUES ('{login}', 'simple', '{password}', '{address}');")
            db.insert(f"INSERT INTO basket(person_login) VALUES ('{login}');")
            db.insert(f"INSERT INTO favorites VALUES ('{login}');")
        session["user_login"] = login

    user_login = session.get("user_login")
    if user_login is None:
        header = 'none'
    else:
        header = 'auth'

    fvr = request.args.get("fvr")
    bsk = request.args.get("bsk")

    if fvr is not None and fvr != "":
        if user_login is None:
            return redirect("/authorization", 301)
        knf_name = fvr
        knife = db.select(f"SELECT * FROM knife k where k.name = '{knf_name}'")
        knife_in = db.select(f"SELECT knife_id FROM favorites_knifes fk "
                             f"where fk.favorites_key = '{user_login}' and fk.knife_id = {knife[0]['id']}")
        if len(knife_in) == 0:
            db.insert(f"INSERT INTO favorites_knifes VALUES ('{user_login}', {knife[0]['id']})")

    if bsk is not None and bsk != "":
        if user_login is None:
            return redirect("/authorization", 301)
        knf_name = bsk
        knife = db.select(f"SELECT * FROM knife k where k.name = '{knf_name}'")
        basket_id = db.select(f"SELECT basket_id from basket b where b.person_login = '{user_login}'")
        knife_in = db.select(f"SELECT knife_id FROM basket_knifes bk "
                             f"where bk.basket_id = {basket_id[0]['basket_id']} and bk.knife_id = {knife[0]['id']}")
        if len(knife_in) == 0:
            db.insert(f"INSERT INTO basket_knifes VALUES ({knife[0]['id']}, {basket_id[0]['basket_id']})")

    companies = db.select("SELECT * FROM company c")
    types = db.select("SELECT * FROM type t")

    knife_type = request.args.get("type")
    company = request.args.get("company")
    price = request.args.get("cool")

    type_search = ""
    company_search = ""
    price_search = ""
    where = ""
    and1 = ""
    and2 = ""

    if knife_type is not None and knife_type != "":
        where = " WHERE "
        type_search = " k.type_name= \'" + knife_type + "\'"
    else:
        knife_type = "all"

    if company is not None and company != "":
        where = " WHERE "
        if knife_type is not None and knife_type != "all":
            and1 = " AND "
        company_search = "k.company_name = \'" + company + "\'"
    else:
        company = "all"

    if price is not None and price != "" and price != 0:
        where = " WHERE "
        if (knife_type is not None and knife_type != "all") or (company is not None and company != "all"):
            and2 = " AND "
        price_search = "k.price <= " + price
    else:
        price = ""

    knifes = db.select(" SELECT * FROM (SELECT * from (SELECT k.name as k_name,"
                       " k.company_name as company_name, k.price as price, k.type_name as type_name"
                       " FROM knife k" + where + type_search + and1 + company_search + and2 + price_search +
                       ") tbl1 inner join company c ON c.name = tbl1.company_name "
                       ") tbl inner join public.type t ON tbl.type_name = t.name ORDER BY tbl.price DESC;")

    context = {
        'priced': price,
        'companied': company,
        'typed': knife_type,
        'knifes': knifes,
        'title': "Главная",
        'companies': companies,
        'types': types,
        'head': header,
        'login': user_login
    }

    return render_template("home_page.html", **context)


@app.route("/favorites")
def favorites():
    user_login = session.get("user_login")
    if user_login is None:
        return redirect('/home', 301)

    to_del = request.args.get("del")
    to_bsk = request.args.get("bsk")

    if to_del != "" and to_del is not None:
        knife_id = db.select(f"SELECT id from knife where name = '{to_del}'")[0]["id"]
        in_fvr = db.select(
            f"SELECT * FROM favorites_knifes WHERE knife_id = {knife_id} and favorites_key = '{user_login}'")
        if len(in_fvr) != 0:
            db.insert(f"DELETE FROM favorites_knifes WHERE favorites_key = '{user_login}' and knife_id = {knife_id}")

    if to_bsk is not None and to_bsk != "":
        knf_name = to_bsk
        knife = db.select(f"SELECT * FROM knife k where k.name = '{knf_name}'")
        basket_id = db.select(f"SELECT basket_id from basket b where b.person_login = '{user_login}'")
        knife_in = db.select(f"SELECT knife_id FROM basket_knifes bk "
                             f"where bk.basket_id = {basket_id[0]['basket_id']} and bk.knife_id = {knife[0]['id']}")
        if len(knife_in) == 0:
            db.insert(f"INSERT INTO basket_knifes VALUES ({knife[0]['id']}, {basket_id[0]['basket_id']})")

    companies = db.select("SELECT * FROM company c")
    types = db.select("SELECT * FROM type t")

    knife_type = request.args.get("type")
    company = request.args.get("company")
    price = request.args.get("cool")

    type_search = ""
    company_search = ""
    price_search = ""
    where = ""
    and1 = ""
    and2 = ""

    if knife_type is not None and knife_type != "":
        where = " WHERE "
        type_search = " k.type_name= \'" + knife_type + "\'"
    else:
        knife_type = "all"

    if company is not None and company != "":
        where = " WHERE "
        if knife_type is not None and knife_type != "all":
            and1 = " AND "
        company_search = "k.company_name = \'" + company + "\'"
    else:
        company = "all"

    if price is not None and price != "" and price != 0:
        where = " WHERE "
        if (knife_type is not None and knife_type != "all") or (company is not None and company != "all"):
            and2 = " AND "
        price_search = "k.price <= " + price
    else:
        price = ""

    user_favorites_relation_knifes = f"(SELECT k.id, k.name, k.company_name, k.type_name, k.price, k.photo_path FROM knife k " \
                                     f"inner join (SELECT knife_id from favorites_knifes fks inner join (SELECT * " \
                                     f"FROM favorites f INNER JOIN (SELECT * FROM person where person.login = \'{user_login}\') prs " \
                                     f"ON f.person_login = prs.login) fvr on fvr.person_login = fks.favorites_key) ids " \
                                     f"on ids.knife_id = k.id) k"

    knifes = db.select(" SELECT * FROM (SELECT * from (SELECT k.name as k_name,"
                       " k.company_name as company_name, k.price as price, k.type_name as type_name"
                       " FROM " + user_favorites_relation_knifes + where + type_search + and1 + company_search + and2 + price_search +
                       ") tbl1 inner join company c ON c.name = tbl1.company_name "
                       ") tbl inner join public.type t ON tbl.type_name = t.name ORDER BY tbl.price DESC;")

    context = {
        'priced': price,
        'companied': company,
        'typed': knife_type,
        'knifes': knifes,
        'title': "Избранное",
        'companies': companies,
        'types': types,
        'login': user_login
    }
    return render_template("favorites.html", **context)


@app.route("/basket")
def basket():
    user_login = session.get("user_login")
    if user_login is None:
        return redirect('/home', 301)

    del_knife_name = request.args.get("del")
    purchase = request.args.get("purchase")

    if purchase == "on":
        basket_id = db.select(f"SELECT basket_id from basket where person_login = '{user_login}'")[0]["basket_id"]
        knife_ids = db.select(f"SELECT knife_id from basket_knifes where basket_id = {basket_id}")
        db.insert(f"INSERT INTO purchase(person_login) VALUES ('{user_login}')")
        purchase_id = db.select(f"SELECT id from purchase ORDER BY id DESC")[0]["id"]
        for kid in knife_ids:
            db.insert(f"DELETE FROM basket_knifes WHERE basket_id = {basket_id} and knife_id = {kid['knife_id']}")
            db.insert(f"INSERT INTO purchase_knifes VALUES ({purchase_id}, {kid['knife_id']} )")

    if del_knife_name != "" and del_knife_name is not None:
        bskt_id = db.select(f"SELECT basket_id from basket where person_login = '{user_login}'")[0]["basket_id"]
        knife_id = db.select(f"SELECT id from knife where name = '{del_knife_name}'")[0]["id"]
        in_bskt = db.select(f"SELECT * FROM basket_knifes WHERE knife_id = {knife_id} and basket_id = {bskt_id}")
        if len(in_bskt) != 0:
            db.insert(f"DELETE FROM basket_knifes WHERE basket_id = {bskt_id} and knife_id = {knife_id}")

    companies = db.select("SELECT * FROM company c")
    types = db.select("SELECT * FROM type t")

    knife_type = request.args.get("type")
    company = request.args.get("company")
    price = request.args.get("cool")

    type_search = ""
    company_search = ""
    price_search = ""
    where = ""
    and1 = ""
    and2 = ""

    if knife_type is not None and knife_type != "":
        where = " WHERE "
        type_search = " k.type_name= \'" + knife_type + "\'"
    else:
        knife_type = "all"

    if company is not None and company != "":
        where = " WHERE "
        if knife_type is not None and knife_type != "all":
            and1 = " AND "
        company_search = "k.company_name = \'" + company + "\'"
    else:
        company = "all"

    if price is not None and price != "" and price != 0:
        where = " WHERE "
        if (knife_type is not None and knife_type != "all") or (company is not None and company != "all"):
            and2 = " AND "
        price_search = "k.price <= " + price
    else:
        price = ""

    user_basket_relation_knifes = f"(SELECT * from knife k INNER JOIN (SELECT knife_id FROM basket_knifes bk " \
                                  f"inner join (SELECT basket_id from basket b where b.person_login= \'{user_login}\') tbl " \
                                  f"ON bk.basket_id = tbl.basket_id) tbl2 ON k.id = tbl2.knife_id) k"

    knifes = db.select(" SELECT * FROM (SELECT * from (SELECT k.name as k_name,"
                       " k.company_name as company_name, k.price as price, k.type_name as type_name"
                       " FROM " + user_basket_relation_knifes + where + type_search + and1 + company_search + and2 + price_search +
                       ") tbl1 inner join company c ON c.name = tbl1.company_name "
                       ") tbl inner join public.type t ON tbl.type_name = t.name ORDER BY tbl.price DESC;")

    context = {
        'priced': price,
        'companied': company,
        'typed': knife_type,
        'knifes': knifes,
        'title': "Корзина",
        'companies': companies,
        'types': types,
        'login': user_login
    }
    return render_template("basket.html", **context)


@app.route("/purchases")
def purchases():
    user_login = session.get("user_login")
    if user_login is None:
        return redirect('/home', 301)

    user_purchases = db.select(f"SELECT * FROM purchase p WHERE p.person_login = '{user_login}' ORDER BY id DESC")
    purch_knifes = []
    for purchase in user_purchases:
        knifes = db.select(f"SELECT * FROM knife inner join (SELECT * from purchase_knifes pk "
                           f"where pk.purchase_id = '{purchase['id']}') upk on knife.id = upk.knife_id ")
        amount = 0
        for knf in knifes:
            amount += int(knf["price"])
        purchase["amount"] = amount
        purch_knifes.append((purchase, knifes))

    context = {
        "title": "Заказы",
        "entity": purch_knifes,
        'login': user_login
    }
    return render_template("purchases.html", **context)


@app.route("/lks", methods=["POST", "GET"])
def lk():
    if request.method == "POST":
        login = session.get("user_login")
        address = request.form.get("address")
        password = request.form.get("password")
        db.insert(f"UPDATE person SET address='{address}', password='{password}' where login = '{login}';")
    user_login = session.get("user_login")
    if user_login is None or user_login == "":
        return redirect('/home', 301)

    person = db.select(f"SELECT * from person where login = '{user_login}'")

    context = {
        "title": "Личный кабинет",
        "person": person[0],
        'login': user_login
    }
    return render_template("lk.html", **context)


@app.route("/lk_change", methods=["post"])
def lk_change():
    user_login = session.get("user_login")
    if user_login is None:
        return redirect('/home', 301)

    context = {
        "title": "Личный кабинет",
        'login': user_login
    }
    return render_template("lk_change.html", **context)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
