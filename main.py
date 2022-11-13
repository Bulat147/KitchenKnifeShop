
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
    # TODO: тут проверить пользователя на авторизоавнность
    user_login = "bulatHulk"

    fvr = request.args.get("fvr")
    bsk = request.args.get("bsk")

    if fvr is not None and fvr != "":
        # TODO: если пользак не авторизован - перекинуть на авторизацию
        knf_name = fvr
        knife = db.select(f"SELECT * FROM knife k where k.name = '{knf_name}'")
        knife_in = db.select(f"SELECT knife_id FROM favorites_knifes fk "
                             f"where fk.favorites_key = '{user_login}' and fk.knife_id = {knife[0]['id']}")
        if len(knife_in) == 0:
            db.insert(f"INSERT INTO favorites_knifes VALUES ('{user_login}', {knife[0]['id']})")


    if bsk is not None and bsk != "":
        # TODO: если пользак не авторизован - перекинуть на авторизацию
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


    if knife_type is not None and knife_type!="":
        where = " WHERE "
        type_search = " k.type_name= \'" + knife_type + "\'"
    else:
        knife_type = "all"

    if company is not None and company!="":
        where = " WHERE "
        if knife_type is not None and knife_type != "all":
            and1 = " AND "
        company_search = "k.company_name = \'" + company +"\'"
    else:
        company = "all"

    if price is not None and price != "" and price != 0:
        where = " WHERE "
        if (knife_type is not None and knife_type != "all") or (company is not None and company != "all"):
            and2 = " AND "
        price_search = "k.price <= "+price
    else:
        price = ""

    knifes = db.select(" SELECT * FROM (SELECT * from (SELECT k.name as k_name,"
                       " k.company_name as company_name, k.price as price, k.type_name as type_name"
                       " FROM knife k"+ where + type_search + and1 + company_search + and2 + price_search +
                       ") tbl1 inner join company c ON c.name = tbl1.company_name "
                       ") tbl inner join public.type t ON tbl.type_name = t.name ORDER BY tbl.price DESC;")

    context = {
        'priced': price,
        'companied': company,
        'typed': knife_type,
        'knifes': knifes,
        'title': "Главная",
        'companies': companies,
        'types': types
    }

    return render_template("home_page.html", **context)


@app.route("/favorites")
def favorites():
    # TODO: тут проверить пользователя на авторизоавнность, иначе перекинуть на другую страничку
    user_login = "bulatHulk"



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


    if knife_type is not None and knife_type!="":
        where = " WHERE "
        type_search = " k.type_name= \'" + knife_type + "\'"
    else:
        knife_type = "all"

    if company is not None and company!="":
        where = " WHERE "
        if knife_type is not None and knife_type != "all":
            and1 = " AND "
        company_search = "k.company_name = \'" + company +"\'"
    else:
        company = "all"

    if price is not None and price != "" and price != 0:
        where = " WHERE "
        if (knife_type is not None and knife_type != "all") or (company is not None and company != "all"):
            and2 = " AND "
        price_search = "k.price <= "+price
    else:
        price = ""

    user_favorites_relation_knifes = f"(SELECT k.id, k.name, k.company_name, k.type_name, k.price, k.photo_path FROM knife k " \
                            f"inner join (SELECT knife_id from favorites_knifes fks inner join (SELECT * " \
                            f"FROM favorites f INNER JOIN (SELECT * FROM person where person.login = \'{user_login}\') prs " \
                            f"ON f.person_login = prs.login) fvr on fvr.person_login = fks.favorites_key) ids " \
                            f"on ids.knife_id = k.id) k"

    knifes = db.select(" SELECT * FROM (SELECT * from (SELECT k.name as k_name,"
                       " k.company_name as company_name, k.price as price, k.type_name as type_name"
                       " FROM "+user_favorites_relation_knifes + where + type_search + and1 + company_search + and2 + price_search +
                       ") tbl1 inner join company c ON c.name = tbl1.company_name "
                       ") tbl inner join public.type t ON tbl.type_name = t.name ORDER BY tbl.price DESC;")

    context = {
        'priced': price,
        'companied': company,
        'typed': knife_type,
        'knifes': knifes,
        'title': "Избранное",
        'companies': companies,
        'types': types
    }
    return render_template("favorites.html", **context)


@app.route("/basket")
def basket():
    # TODO: тут проверить пользователя на авторизоавнность, иначе перекинуть на другую страничку
    user_login = "bulatHulk"



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


    if knife_type is not None and knife_type!="":
        where = " WHERE "
        type_search = " k.type_name= \'" + knife_type + "\'"
    else:
        knife_type = "all"

    if company is not None and company!="":
        where = " WHERE "
        if knife_type is not None and knife_type != "all":
            and1 = " AND "
        company_search = "k.company_name = \'" + company +"\'"
    else:
        company = "all"

    if price is not None and price != "" and price != 0:
        where = " WHERE "
        if (knife_type is not None and knife_type != "all") or (company is not None and company != "all"):
            and2 = " AND "
        price_search = "k.price <= "+price
    else:
        price = ""

    user_basket_relation_knifes = f"(SELECT * from knife k INNER JOIN (SELECT knife_id FROM basket_knifes bk " \
                                  f"inner join (SELECT basket_id from basket b where b.person_login= \'{user_login}\') tbl " \
                                  f"ON bk.basket_id = tbl.basket_id) tbl2 ON k.id = tbl2.knife_id) k"


    knifes = db.select(" SELECT * FROM (SELECT * from (SELECT k.name as k_name,"
                       " k.company_name as company_name, k.price as price, k.type_name as type_name"
                       " FROM "+user_basket_relation_knifes + where + type_search + and1 + company_search + and2 + price_search +
                       ") tbl1 inner join company c ON c.name = tbl1.company_name "
                       ") tbl inner join public.type t ON tbl.type_name = t.name ORDER BY tbl.price DESC;")

    context = {
        'priced': price,
        'companied': company,
        'typed': knife_type,
        'knifes': knifes,
        'title': "Корзина",
        'companies': companies,
        'types': types
    }
    return render_template("basket.html", **context)


@app.route("/purchases")
def purchases():
    # TODO: тут проверить пользователя на авторизоавнность, иначе перекинуть на другую страничку
    user_login = "bulatHulk"

    user_purchases = db.select(f"SELECT * FROM purchase p WHERE p.person_login = '{user_login}'")
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
        "entity": purch_knifes
    }
    return render_template("purchases.html", **context)

@app.route("/lk")
def lk():
    # TODO: тут проверить пользователя на авторизоавнность, иначе перекинуть на другую страничку
    user_login = "bulatHulk"

    person = db.select(f"SELECT * from person where login = '{user_login}'")

    context = {
        "title": "Личный кабинет",
        "person": person[0]
    }
    return render_template("lk.html", **context)

@app.route("/lk_change", methods=["post"])
def lk_change():
    # TODO: тут проверить пользователя на авторизоавнность, иначе перекинуть на другую страничку
    user_login = "bulatHulk"

    context = {
        "title": "Личный кабинет"
    }
    return render_template("lk_change.html", **context)



if __name__ == '__main__':
    app.run(port=8000, debug=True)