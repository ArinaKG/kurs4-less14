import json
import sqlite3
import flask
import tmp as tmp

app = flask.Flask(__name__)


def get_value_from_db(sql):
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row

        result = connection.execute(sql).fetchall()

        return result


@app.get("/movie/<title>")
def get_value_by_title(title):
    sql = (f'select title, country, release_year, listed_in as genre, description from netflix\'\n'
           f'    where title = \'{title}\'\n'
           f'    order by release_year desc\n'
           f'    limit 1\n'
           f'    ')

    result = get_value_from_db(sql)

    for item in result:
        return dict(item)


@app.get("/movie/<title>")
def view_title(title):
    result = get_value_by_title(title)
    return app.response_class(
        response=json.dumps(result,
                            ensure_ascii=False,
                            indent=4
                            ),
        status=200,
        mimetype="application/json"

    )


@app.get("/movie/<int:year1>/to/<int:year2>")
def det_by_date(year1, year2):
    sql = f'''
            select title, release_year from netflix
            where release_year between {year1} and {year2}
            limit 100'''
    result = get_value_from_db(sql)

    tmp = []
    for item in result:
        tmp.append(dict(item))
    return app.response_class(
        response=json.dumps(tmp,
                            ensure_ascii=False,
                            indent=4
                            ),
        status=200,
        mimetype="application/json"

    )


@app.get("/rating/<rating>")
def get_by_rating(rating):
    my_dict= ("children": ("G"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    )


    sql = f'''
            select title, rating, description from netflix
            where rating in {my_dict.get(rating), ("G", "NC-17")}'''
    result = get_value_from_db(sql)

    tmp = []
    for item in result:
        tmp.append(dict(item))
    return app.response_class(
        response=json.dumps(tmp,
                            ensure_ascii=False,
                            indent=4
                            ),
        status=200,
        mimetype="application/json"

    )


@app.get("/genre/<genre>")
def get_by_genre(genre):
    sql = f'''
            select title, description from netflix
            where listed_in like 'genre' '''

    result = get_value_from_db(sql)

    tmp = []
    for item in result:
        tmp.append(dict(item))

    return app.response_class(
        response=json.dumps(tmp,
                            ensure_ascii=False,
                            indent=4
                            ),
        status=200,
        mimetypes='application/json'

    )


def get_by_names(name1, name2, tmp=None):
    sql = f'''
    select * from netflix
where "cast" like '%{name1}%' and "cast" like '%{name2}%' '''

    result = get_value_from_db(sql)

    names_dict = {}
    for item in result
        names = set(dict(item).get("cast").split(", ")) - set(name1, name2)

        for name in names:
            names_dict[name.strip()] = names_dict.get(name.strip, 0) + 1

    for key, value in names_dict.items():
        if value >2:
            tmp.append(key)
            
    return tmp


def get_ditales(typ, year, genre):
    sql = f'''
        select * from netflix
        where type = '{typ}' and
        release_year = '{year}' and
        listed_in like '%{genre}%'
'''

    result = get_value_from_db(sql)

    tmp = []
    for item in result:
        tmp.append(dict(item))

    return json.dumps(tmp,
                            ensure_ascii=False,
                            indent=4
                            )



if __name__ == '__main__':
    app.run(debug=True)
