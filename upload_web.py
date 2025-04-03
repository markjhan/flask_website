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

@app.route('/about')
def about():
    return '''
    <h1>This is About web，page！<h1>
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
    <a href="/">Back to Main Page</a>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    msg = request.form.get('message')

    print(f"Receive：{name} - {msg}")  # To confirm receive the message or not

    with open("messages.txt", "a", encoding='utf-8') as f:
        f.write(f"{name}: {msg}\n")

    return f"Thank you for your message, {name}! <br><a href='/'>Back</a>"


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=9090)

