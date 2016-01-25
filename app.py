from flask import Flask
from flask import render_template
from flask import request

from dateparser import DateParser


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        dp = DateParser()
        content = request.form.get('content')
        if content:
            result = dp.parse(content)
    return render_template('test_form.html', result=result, content=content)

if __name__ == '__main__':
    app.run(debug=True)
