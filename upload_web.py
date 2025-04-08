from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>this is main page<h1>
    <a href="https://www.google.com" target='_blank'>go to google</a> >:)<br>
    <a href="/about"> go to about page </a><br>
    <a href="/message">Leave some message</a><br>
    '''

@app.route('/secret')
def secret():
    return '''
    <h1>You find the secret page!<h1>
    <form action="/dunbar" method="POST">
        Your Name: <br>
        <input type="text" name="name"><br><br>
        
        SecretMessage: <br>
        <textarea name="secret message" rows="4" cols="40"></textarea><br><br>
        
        <input type="submit" value="Submit">
    </form>
    <br>
    <a href="/">Back to Main Page</a>
    '''

@app.route('/dunbar', methods=['POST'])
def dunbar():
    name = request.form.get('name')
    msg = request.form.get('secret message')

    print(f"Receive：{name} - {msg}")

    with open("secret_messages.txt", "a", encoding='utf-8') as f:
        f.write(f"{name} - {msg}\n")

    return f"Thank you for your secret, {name}! <br><a href='/'>Back to Main Page</a>"

@app.route('/about')
def about():
    return '''
    <h1>This is About page！<h1>
    <a href="/">back to main page</a>
    '''

@app.route('/message')
def message():
    return '''
    <h1>Message Board</h1>
    <form action="/submit" method="POST">
        Your Name：<br>
        <input type="text" name="name"><br><br>

        Message：<br>
        <textarea name="message" rows="4" cols="40"></textarea><br><br>

        <input type="submit" value="Submit">
    </form>
    <br>
    <a href="/">Back to Main Page</a><br>
    <a href="/sure">Something else here(?)</a>
    '''

@app.route('/sure')
def sure():
    return '''
    <h1>ARE YOU SURE YOU WANT TO SEE  THIS PAGE??<h1><br>
    <a href="/secret">I AM SURE</a>'''
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    msg = request.form.get('message')

    print(f"Receive：{name} - {msg}")  # To confirm receive the message or not

    with open("messages.txt", "a", encoding='utf-8') as f:
        f.write(f"{name}: {msg}\n")

    return f"Thank you for your message, {name}! <br><a href='/'>Back</a>"


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

