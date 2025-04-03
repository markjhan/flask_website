from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>this is main page<h1>
    <a href="https://www.google.com" target='_blank'>go to google</a> >:)<br>
    <a href="/about"> go to about page </a>
    <a href="/message">我要留言</a><br>
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
    <h1>留言板</h1>
    <form action="/submit" method="POST">
        你的名字：<br>
        <input type="text" name="name"><br><br>

        留言内容：<br>
        <textarea name="message" rows="4" cols="40"></textarea><br><br>

        <input type="submit" value="提交留言">
    </form>
    <br>
    <a href="/">返回主页</a>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    msg = request.form.get('message')

    with open("messages.txt", "a", encoding='utf-8') as f:
        f.write(f"{name}：{msg}\n")

    return f"谢谢你的留言，{name}！<br><a href='/'>返回主页</a>"


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=9090)

