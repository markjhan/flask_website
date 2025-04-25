from flask import Flask, render_template, request, json

app = Flask(__name__)
app.config['Secret_Mode'] = False
app.config['get_secret'] = False

def analyze_message(messages):
    emotional_keywords = ["sad", "upset", "tired"]
    programming_keywords = ["python", "flask", "code"]
    question_keywords = ["how", "what", "?", "help"]
    messages = messages.lower()
    if any(w in messages for w in emotional_keywords):
        label = "feeling down"
        reply = "I'm here for you. You're not along."

    elif any(w in messages for w in programming_keywords):
        label = "programming"
        reply = "Python is a great choice. You're doing amazing!"

    elif any(w in messages for w in question_keywords):
        label = "Ask question"
        reply = 'Not sure where to start? Try visiting the message page or the about section.'

    else:
        label = "simple"
        reply = "Thank you for your message. I appreciate your visit!"

    return label, reply

@app.route('/')
def home():
    app.config['Secret_Mode'] = False
    return '''
    <h1>this is main page<h1>
    <a href="/about">Go to About Page </a><br>
    <a href="/message">Go to Message Page</a><br>
    <a href="/search">Go to Search Page</a>
    '''

@app.route('/search')
def search():
    return '''
    <h1>Search Something</h1>
    <form action="/search_result" method="POST">
        Search: <br>
        <textarea name="search" rows="4" cols="40"></textarea><br><br>
        
        <input type="submit" value="Search">
    </form>
    <br>
    <a href='/'>Back to Main Page</a>
    '''

@app.route('/search_result', methods=['POST'])
def search_result():
    msg = request.form.get("search").strip().lower()
    matches = []

    search_index = [
       {
           'title':'About this website',
            'url':'/about',
            'content':'This website is built with Flask. I built this when I was 17.'
        },
       {
           'title':'Message Page',
           'url':'/message',
           'content':'Leave your message.'
       },
       {
           'title':'Secret Page',
           'url':'/secret',
           'content':'Leave secret message. Secret message will not show on the past messages board.'
       },
       {
           'title':'All Past Messages',
           'url':'/past',
           'content':'View all past messages.'
       },
       {
           'title':'Latest Message',
           'url':'/latest',
           'content':'Check the latest message'
       },
       {
           'title':'Get Message by Code',
           'url':'/get_secret',
           'content':'Get the secret messages by a code.'
       }
    ]

    for result in search_index:
       combined_text = (result['title'] + ' ' + result['content']).lower()
       if msg in combined_text:
           matches.append(result)

    html = ""

    for match in matches:
       html += f"<p><a href={match['url']}>{match['title']}</a></p>"

    if html:
        return f'''
        <h2>Search Results:</h2><br>
        {html}<br><br>
        <h3><a href='/'>Back to Main Page</a></h3>
        '''
    else:
        return '''
        <h2>No results found</h2><br><br>
        <h3><a href='/'>Back to Main Page</a></h3>
        '''

@app.route('/secret')
def secret():
    app.config['Secret_Mode'] = True
    app.config['get_secret'] = False
    return '''
    <head><title>Secret Page</title></head>
    <h2>
    <form action="/submit" method="POST">
        Your Name: <br>
        <input type="text" name="name"><br><br>
        
        SecretMessage: <br>
        <textarea name="secret message" rows="4" cols="40"></textarea><br><br>
        
        Secret Code: <br>
        <input type="text" name="code"><br><br>
        
        <input type="submit" value="Submit"><br><br>
    </form>
    </h2>
    <h2>Secret messages will not show on the past messages page.<h2>
    <br>
    <a href="/message">Back to Message Page</a>
    '''

@app.route('/get_message')
def get_secret_message():
    app.config['get_secret'] = True
    app.config['Secret_Mode'] = False
    return '''
    <head><title>Get</title></head>
    <h1>Enter the code to get secret messages</h1>
    <h2>
    <form action="/submit" method="POST">
        Secret Code: <br>
        <input type="text" name="code"><br><br>
        
        <input type="submit" value="Submit"><br><br>
    <form>
    <a href='/message'>Back</a>
    </h2>
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

    cleaned_lines += """
    <br><a href='/message'>Back to Message Page</a>
    """
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
        My hobby is playing the guitar, travelling, and trying different kinds of food.<br>
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
    app.config['get_secret'] = False
    app.config['Secret_Mode'] = False
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
    <a href="/secret">Send a Secret Message</a><br>
    <a href="/latest">Check the latest message</a><br>
    <a href='/past'>View All Past Messages</a><br>
    <a href='/get_message'>Get Messages by Code</a>
    '''

@app.route('/latest')
def show_latest_message():
    try:
        with open("messages.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            if lines:
                last_message = lines[-2].strip()
            else:
                last_message = "(No messages yet.)"
    except FileNotFoundError:
        last_message = "(No messages yet.)"

    return f'''
    <head><title>Latest Message</title></head>
    <h2>Latest message:</h2><p>{last_message}</p><br>
    <a href='/message'>Back to Message Page</a>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    if not app.config['Secret_Mode'] and not app.config['get_secret']:
        name = request.form.get('name')
        msg = request.form.get('message')

        print(f"Receive：{name} - {msg}")  # To confirm receive the message or not

        app.config["Secret_Mode"] = False

        label, reply = analyze_message(msg)

        new_entry = {
            "name": name,
            "message": msg,
            "label": label,
            "reply": reply
        }

        try:
            with open("messages.json", "r", encoding="utf_8") as f:
                all_messages = json.load(f)
        except FileNotFoundError:
            all_messages = []

        all_messages.append(new_entry)

        with open("messages.json", "w", encoding="utf-8") as f:
            json.dump(all_messages, f, indent=2, ensure_ascii=False)

        # with open("messages.txt", "a", encoding='utf-8') as f:
        #     f.write(f"{name}: {msg} [Label : {label}]\n")
        #     f.write(f"Bot: {reply}\n")
            
        return f"""
        <h2>Message received!</h2><br>
        <p><strong>You said: </strong>{msg}</p>
        <p><strong>Bot replied: </strong>{reply}</p>
        <a href='/message'>Back</a>"""

    elif app.config['Secret_Mode'] and not app.config['get_secret']:
        name = request.form.get('name')
        msg = request.form.get('secret message')
        code = request.form.get('code')

        print(f"Receive：{name} - {msg}")

        with open("secret_messages.txt", "a", encoding='utf-8') as f:
            f.write(f"{name} : {msg} ---- Code:{code}\n")

        app.config["Secret_Mode"] = False

        return f"Thank you for your secret, {name}! <br><a href='/message'>Back to Message Page</a>"

    elif app.config['get_secret'] and not app.config['Secret_Mode']:
        code_input = request.form.get("code").strip()
        if code_input:
            matches = []
            try:
                with open("secret_messages.txt", "r", encoding='utf-8') as f:
                    for line in f:
                        if f"Code:{code_input}" in line:
                            cleaned_line = line.replace(f" ---- Code:{code_input}", "")
                            print(cleaned_line)
                            matches.append(cleaned_line.strip())

            except FileNotFoundError:
                return '<p>No message found yet.</p>'

            if matches:
                result_html = f"<h2>Message for Code: {code_input}</h2>"
                for msg in matches:
                    result_html += f"<h3><p>{msg}</p></h3>"

            else:
                return '''
                <p>No message found for this code.</p><br>
                <a href='/message'>Back to Message Page</a>
                '''

            result_html += "<a href='/message'>Back to Message Page</a>"
            return result_html
        else:
            return '''
            <p>Please enter a code.</p><br>
            <a href='/get_message'>Back</a>
            '''


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='localhost', port=9090)

