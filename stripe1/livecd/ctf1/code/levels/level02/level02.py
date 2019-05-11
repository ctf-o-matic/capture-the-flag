#!/usr/bin/env python
#
import flask
from flask import request, make_response, render_template
import os
import random
import string

PORT = 8002

app = flask.Flask(__name__)

wwwdata_dir = os.path.join(os.path.dirname(__file__), 'wwwdata')
if not os.path.isdir(wwwdata_dir):
    os.makedirs(wwwdata_dir)


def random_string(length):
    return ''.join(random.choice(string.letters) for i in xrange(length))


@app.route('/', methods=['GET', 'POST'])
def index():
    params = {}
    if request.method == 'POST':
        params['name'] = request.form.get('name')
        params['age'] = request.form.get('age')

    user_details = request.cookies.get('user_details')
    if not user_details:
        params['out'] = 'Looks like a first time user. Hello, there!'
        filename = random_string(16) + '.txt'
        path = os.path.join(wwwdata_dir, filename)
        f = open(path, 'w')
        f.write('%s is using %s\n' % (request.remote_addr, request.user_agent))
        resp = make_response(render_template('index.html', **params))
        resp.set_cookie('user_details', filename)
    else:
        filename = user_details
        path = os.path.join(wwwdata_dir, filename)
        params['out'] = open(path).read()
        resp = make_response(render_template('index.html', **params))
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
