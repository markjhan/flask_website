from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return '''
    <h1>this is main page<h1>
    <a href="https://www.google.com" target='_blank'>go to google</a> >:)<br>
    <a href="/about"> go to about page </a>

    '''


@app.route('/about')
def about():
    return '''
    <h1>This is About web，page！<h1>
    <a href="/">back to main page</a>
    '''


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port = port)