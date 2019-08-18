#!/usr/bin/env python2

import os
import sqlite3
import sys

import flask
from flask import request, make_response, render_template

PORT = int(sys.argv[1])
WWWDATA_DIR = sys.argv[2]
DATABASE = os.path.join(WWWDATA_DIR, 'db.sqlite3')


app = flask.Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    sql = "SELECT * FROM safemedicalanalysis_medicalresult WHERE patient_id = 7"

    if request.method == 'POST':
        sql += " AND description LIKE '%{}%'".format(request.form.get('search_box'))

    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute(sql)
    names = [x[0] for x in cur.description]
    rows = cur.fetchall()
    context = {"results": [dict(zip(names, rx)) for rx in rows]}

    return make_response(render_template('index.html', **context))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
