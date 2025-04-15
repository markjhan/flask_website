from flask import Flask, render_template, request

app = Flask(__name__)
app.config['Secret_Mode'] = False

@app.route('/')
def home():
    app.config['Secret_Mode'] = False
    return '''
    <h1>this is main page<h1>
    <a href="/about">Go to About Page </a><br>
    <a href="/message">Go to Message Page</a><br>
    '''

@app.route('/secret')
def secret():
    app.config['Secret_Mode'] = True
    return '''
    <head><title>Secret Page</title></head>
    <h1>You find the secret page!<h1>
    <form action="/submit" method="POST">
        Your Name: <br>
        <input type="text" name="name"><br><br>
        
        SecretMessage: <br>
        <textarea name="secret message" rows="4" cols="40"></textarea><br><br>
        
        <input type="submit" value="Submit">
    </form>
    <h2>Secret messages will not show on the past messages page.<h2>
    <br>
    <a href="/">Back to Main Page</a><br>
    <a href="/message">Back to Message Page</a>
    '''

@app.route('/past')
def show_past_messages():
    try:
        with open("messages.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            if lines:
                all_past_messages = [line.strip() for line in lines]
            else:
                all_past_messages = "(No messages yet)"
    except FileNotFoundError:
        all_past_messages = "(No messages yet)"

    cleaned_lines ="<h2>All Past Messages: </h2>"

    for line in all_past_messages:
        cleaned_lines += f"<p>{line}</p>"

    cleaned_lines += "<br><a href='/'>Back to Main Page</a>"
    return f'''
    <head><title>All Past Messages</title></head>
    {cleaned_lines}
    '''

@app.route('/about')
def about():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
    <title>About This Website</title>
    </head>
    <body>
    <h1>About This Website</h1>

    <p>
        I built this website as part of my journey into programming.
    </p>

    <p>
        This project is my first step into web development.
        I used Python and Flask to build a simple website where users can leave messages.
        The idea may be small, but it's completely mine — written, tested, and deployed by me. 
        The most interesting part is that I learned all of these with chatGPT, and I would like to say it is the best teacher.
    </p>

    <p>
        I plan to improve this site over time, adding features like a message board, chatbot responses, and even AI tools.
        For now, it's proof that even without a traditional school path, I can learn and build.
    </p>

    <h1>About Me</h1>
    
    <p>
        Hi, I'm someone who left school in 8th grade and have been self-studying ever since.<br>
        I started learning Python because I wanted to create real things, not just follow tutorials.<br>
        My hobby is playing the guitar, travelling, and trying different kings of food.<br>
        I used to live in Japan for 6 months just by my self, and I'm now living in Vancouver, BC alone as well.<br>
        I'm really proud of myself, cause I applied the visa on my own, and it successfully been approved.<br>
        I was 17 when I wrote all of these. I hope you like this website.<br>
    </p>
    
    <p>
        <h3>Thank you for visiting.<h3>
        <h6>----Written on April 13th, 2025.<h6>
    </p>
    
    </body>
    </html>

    <a href="/">Back to Main Page</a>
    '''

@app.route('/message')
def message():
    return '''
    <head>
    <title>Message Board</title>
    </head>
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
    <a href="/sure">Something else here(?)</a><br>
    <a href="/latest">Check the latest message</a><br>
    <a href='/past'>View All Past Messages</a>
    '''

@app.route('/sure')
def sure():
    return '''
    <head><title>CONFIRM</title></head>
    <h1>ARE YOU SURE YOU WANT TO SEE  THIS PAGE??<h1><br>
    <a href="/secret">I AM SURE</a>'''

@app.route('/latest')
def show_latest_message():
    try:
        with open("messages.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            if lines:
                last_message = lines[-1].strip()
            else:
                last_message = "(No messages yet.)"
    except FileNotFoundError:
        last_message = "(No messages yet.)"

    return f'''
    <head><title>Latest Message</title></head>
    <h2>Latest message:</h2><p>{last_message}</p><br><a href='/message'>Back to Message Page</a>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    if not app.config['Secret_Mode']:
        name = request.form.get('name')
        msg = request.form.get('message')

        print(f"Receive：{name} - {msg}")  # To confirm receive the message or not

        app.config["Secret_Mode"] = False

        with open("messages.txt", "a", encoding='utf-8') as f:
            f.write(f"{name}: {msg}\n")

        reply = f"Hi {name}, thank you for your message! I'm just a simple robot, but I wish you have a good day."

        with open("messages.txt", "a", encoding='utf-8') as f:
            f.write(f"Bot: {reply}")
            
        return f"""
        <h2>Message received!</h2><br>
        <p><strong>You said: </strong>{msg}</p>
        <p><strong>Bot replied: </strong>{reply}</p>
        <a href='/'>Back</a>"""

    elif app.config['Secret_Mode']:
        name = request.form.get('name')
        msg = request.form.get('secret message')

        print(f"Receive：{name} - {msg}")

        with open("secret_messages.txt", "a", encoding='utf-8') as f:
            f.write(f"{name} : {msg}\n")

        app.config["Secret_Mode"] = False

        return f"Thank you for your secret, {name}! <br><a href='/'>Back to Main Page</a>"



if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

