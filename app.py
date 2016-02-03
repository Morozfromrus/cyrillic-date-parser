# -*- coding: utf-8 -*-

from __future__ import print_function

import os

from flask import Flask
from flask import render_template
from flask import request
from dateparser import DateParser


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    content = ''
    history = []
    filename = '/tmp/datetime-parser-history.txt'
    if os.path.isfile(filename):
        hf = open(filename, 'r+')
    else:
        hf = open(filename, 'w+')
    for hi in hf:
        history.append(hi.decode('utf-8').strip('\n'))
    hf.close()
    content = request.values.get('content')
    if content:
        dp = DateParser()
        if content in history:
            history.remove(content)
        history.append(content)
        result = dp.parse(content)

    hf = open(filename, 'w')
    for hi in history:
        print(hi.encode('utf-8'), file=hf)
    hf.close()

    history.reverse()
    history = history[:500]
    return render_template('test_form.html', result=result, content=content, history=history)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8083)
