from flask import Flask, render_template, request, json, session, redirect
import random

app = Flask(__name__)
app.secret_key = "admin1234"

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
    return '''
    <h1>
    This is main page<br>
    <a href="/about">Go to About Page </a><br>
    <a href="/message">Go to Message Page</a><br>
    <a href="/search">Go to Search Page</a><br>
    <a href="/easter_egg">Get a surprise</a><br>
    </h1>
    '''

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        msg = request.form.get("search").strip().lower()
        matches = []

        search_index = [
            {
                'title': 'About this website',
                'url': '/about',
                'content': 'This website is built with Flask. I built this when I was 17.'
            },
            {
                'title': 'Message Page',
                'url': '/message',
                'content': 'Leave your message.'
            },
            {
                'title': 'Secret Page',
                'url': '/secret',
                'content': 'Leave secret message. Secret message will not show on the past messages board.'
            },
            {
                'title': 'Get message by name',
                'url': '/search_by_name',
                'content': 'search message by a name.'
            },
            {
                'title': 'Latest Message',
                'url': '/latest',
                'content': 'Check the latest message'
            },
            {
                'title': 'Get Secret Message by Code',
                'url': '/get_message',
                'content': 'Get the secret messages by a code.'
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

    return '''     
        <h1>Search Something</h1>
        <form method="POST">
            Search: <br>
            <textarea name="search" rows="4" cols="40"></textarea><br><br>

            <input type="submit" value="Search">
        </form>
        <br>
        <a href='/'>Back to Main Page</a>
        '''

@app.route('/secret', methods=['GET','POST'])
def secret():
    if request.method == 'POST':
        name = request.form.get('name')
        msg = request.form.get('secret message')
        code = request.form.get('code')

        print(f"Receive：{name} - {msg} - {code}")

        new_entry = {
            "name": name,
            "message": msg,
            "code": code
        }

        try:
            with open("secret_messages.json", "r", encoding="utf_8") as f:
                all_messages = json.load(f)
        except FileNotFoundError:
            all_messages = []

        all_messages.append(new_entry)

        with open("secret_messages.json", "w", encoding="utf-8") as f:
            json.dump(all_messages, f, indent=2, ensure_ascii=False)

        return f"Thank you for your secret, {name}! <br><a href='/message'>Back to Message Page</a>"

    return '''
    <head><title>Secret Page</title></head>
    <h2>
    <form method="POST">
        Your Name: <br>
        <input type="text" name="name"><br><br>
        
        SecretMessage: <br>
        <textarea name="secret message" rows="4" cols="40"></textarea><br><br>
        
        Secret Code: <br>
        <input type="password" name="code"><br><br>
        
        <input type="submit" value="Submit"><br><br>
    </form>
    </h2>
    <h2>Secret messages will not show on the past messages page.<h2>
    <br>
    <a href="/message">Back to Message Page</a>
    '''

@app.route('/get_message', methods=['GET','POST'])
def get_secret_message():
    if request.method == 'POST':
        code_input = request.form.get("code").strip()
        if code_input:
            matches = []
            try:
                with open("secret_messages.json", "r", encoding='utf-8') as f:
                    all_messages = json.load(f)
                    for object in all_messages:
                        if object['code'] == code_input:
                            matches.append(object['name'] + " : " + object['message'])

            except FileNotFoundError:
                return '<p>No message found yet.</p>'

            if matches:
                result_html = f"<h2>Message for Code: {code_input}</h2>"
                for msg in matches:
                    result_html += f"<h3><p>{msg}</p></h3>"

            else:
                return '''
                        <p>No message found for this code.</p><br>
                        <a href='/get_message'>Back</a>
                        '''

            result_html += "<a href='/get_message'>Back</a>"
            return result_html
        else:
            return '''
                    <p>Please enter a code.</p><br>
                    <a href='/get_message'>Back</a>
                    '''

    return '''
    <head><title>Get</title></head>
    <h1>Enter the code to get secret messages</h1>
    <h2>
    <form method="POST">
        Secret Code: <br>
        <input type="password" name="code"><br><br>
        
        <input type="submit" value="Submit"><br><br>
    </form>
    <a href='/message'>Back</a>
    </h2>
    '''
@app.route('/search_by_name', methods=['GET', 'POST'])
def search_by_name():
    if request.method == 'POST':
        search_name = request.form.get("search name").lower().strip()
        if search_name:
            matches = []
            try:
                with open("messages.json", "r", encoding="utf-8") as f:
                    all_messages = json.load(f)

                    for result in all_messages:
                        name = (result['name']).lower()
                        if search_name == name.lower():
                            matches.append(result)

                if matches:
                    html = "<h2>Search Results:</h2><br><br>"
                    for match in matches:
                        html += f"<p>{match['message']}</p>"
                    html += "<br><br><a href='/search_by_name'>Back</a>"
                    return html

                else:
                    return '''
                            <h2>No messages found for this name.</h2>
                            <br><a href='/search_by_name'>Back</a>
                            '''
            except FileNotFoundError:
                return '''
                        <h2>No message data found.</h2>
                        <br><a href='/message'>Back</a>
                        '''
        else:
            return '''
                        <h2>Please enter a name.</h2>
                        <br><a href='/search_by_name'>Back</a>
                        '''

    return '''
    <h1>Enter the Name</h1>
    <h2>
    <form method="POST">
        Name: <br>
        <input type="text" name="search name"><br><br>
        
        <input type="submit" value="Submit"><br><br>
    </form>
    <a href="/message">Back</a>
    </h2>
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

@app.route('/message', methods=['GET','POST'])
def message():
    if request.method == 'POST':
        name = request.form.get('name')
        msg = request.form.get('message')

        if name and msg:
            print(f"Receive：{name} - {msg}")  # To confirm receive the message or not

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
        else:
            return '''
                    <h2>Please enter your name and message.</h2><br>
                    <a href='/message'>Back</a>
                    '''

        return f"""
                <h2>Message received!</h2><br>
                <p><strong>You said: </strong>{msg}</p>
                <p><strong>Bot replied: </strong>{reply}</p>
                <a href='/message'>Back</a>"""

    return '''
    <head>
    <title>Message Board</title>
    </head>
    <h1>Message Board</h1>
    <form method="POST">
        Your Name:<br>
        <input type="text" name="name"><br><br>

        Message:<br>
        <textarea name="message" rows="4" cols="40"></textarea><br><br>

        <input type="submit" value="Submit">
    </form>
    <br>
    <a href="/">Back to Main Page</a><br>
    <a href="/secret">Send a Secret Message</a><br>
    <a href="/latest">Check the latest message</a><br>
    <a href='/get_message'>Get Messages by Code</a><br>
    <a href='/search_by_name'>Search Messages by name</a><br>
    <a href='/topic'>Go to Topic Main Page</a><br>
    '''

@app.route('/topic')
def topic():
    return '''
    <head><title>Topic Main Page</title></head>
    <h1>Topic Main Page</h1>
    <h2><a href='/topic_message'>Leave Messages with Topic</a><br><br>
    <a href='/topic_view'>View and Search Messages with Topic</a><br><br>
    <a href='/topic_admin'>Admin Page</a><br><br>
    <a href='/message'>Back</a><br></h2>
    '''

@app.route('/topic_message', methods=['GET', 'POST'])
def topic_message():
    if request.method == 'POST':
        name = request.form.get('name_topic')
        msg = request.form.get('message_topic')
        topics = request.form.get('topic')

        if name and msg and topics:
            print(f"Receive：{name} - {msg} - {topics}")

            new_entry = {
                "name": name,
                "message": msg,
                "topic": topics
            }

            try:
                with open("messages_topic.json", "r", encoding="utf_8") as f:
                    all_messages = json.load(f)
            except FileNotFoundError:
                all_messages = []

            all_messages.append(new_entry)

            with open("messages_topic.json", "w", encoding="utf-8") as f:
                json.dump(all_messages, f, indent=2, ensure_ascii=False)
        else:
            return '''
                    <h2>Please fill in all fields.</h2><br>
                    <a href='/topic_message'>Back</a>
                    '''
        return f"""
                        <h2>Message received!</h2><br>
                        <a href='/topic'>Back</a>"""

    return '''
    <head>
    <title>Topic Message Board</title>
    </head>
    <h1>Topic Message Board</h1>
    <form method="POST">
        Your Name:<br>
        <input type="text" name="name_topic"><br><br>

        Message:<br>
        <textarea name="message_topic" rows="4" cols="40"></textarea><br><br>
        
        Topic:<br>
        <input type="text" name="topic"><br><br>

        <input type="submit" value="Submit">
    </form><br>
    <a href="/topic">Back</a><br>
    '''

@app.route('/topic_view', methods=['GET', 'POST'])
def topic_view():
    if request.method == 'POST':
        search_topic = request.form.get("search topic").lower().strip()
        if search_topic:
            matches = []
            try:
                with open("messages_topic.json", "r", encoding="utf-8") as f:
                    all_messages = json.load(f)

                    for result in all_messages:
                        topics = (result['topic']).lower()
                        if search_topic == topics.lower():
                            matches.append(result)

                if matches:
                    html = "<h2>Search Results:</h2><br><br>"
                    for match in matches:
                        html += f"<p><strong>{match['topic']}</strong> -- {match['message']}</p>"
                    html += "<br><br><a href='/topic_view'>Back</a>"
                    return html

                else:
                    return '''
                            <h2>No messages found for this topic.</h2>
                            <br><a href='/topic_view'>Back</a>
                            '''
            except FileNotFoundError:
                return '''
                        <h2>No message data found.</h2>
                        <br><a href='/topic'>Back</a>
                        '''
        else:
            return '''
                        <h2>Please enter a topic.</h2>
                        <br><a href='/topic'>Back</a>
                        '''

    msgs = []
    try:
        with open("messages_topic.json", "r", encoding="utf-8") as f:
            all_messages = json.load(f)
        for result in all_messages:
            msg = (result['message'])
            msgs.append(msg)
    except FileNotFoundError:
        msgs = "(No messages yet.)"
    msg_html = "<br>".join(msgs)
    return f'''
        <h1>Enter a Topic</h1>
        <h2>
        <form method="POST">
            Topic: <br>
            <input type="text" name="search topic"><br><br>

            <input type="submit" value="Submit">
        </form>
        <a href="/topic">Back</a><br><br><br><br>
        {msg_html}<br>
        </h2>
        '''

@app.route('/topic_admin')
def topic_admin():
    if not session.get("admin_logged_in"):
        return redirect("/password_admin")

    with open("messages_topic.json", "r", encoding="utf-8") as f:
        all_messages = json.load(f)

    html = "<h2>Admin Panel: Manage Messages</h2><br>"
    for idx, msg in enumerate(all_messages):
        html += f"<p><strong>{msg['name']}</strong>: {msg['message']} -- {msg['topic']}</p>"
        html += f'''
            <form method="POST" action="/delete/{idx}">
                <input type="submit" value="Delete">
            </form>
        '''
    html += "<br><a href='/logout_admin'>Log out</a>"
    return html

@app.route("/delete/<int:idx>", methods=["POST"])
def delete_message(idx):
    if not session.get("admin_logged_in"):
        return redirect("/password_admin")

    try:
        with open("messages_topic.json", "r", encoding="utf-8") as f:
            all_messages = json.load(f)

        if 0 <= idx < len(all_messages):
            all_messages.pop(idx)

        with open("messages_topic.json", "w", encoding="utf-8") as f:
            json.dump(all_messages, f, indent=2, ensure_ascii=False)

    except FileNotFoundError:
        pass

    return redirect("/topic_admin")

@app.route('/password_admin', methods=["GET", "POST"])
def password_admin():
    if request.method == "POST":
        if request.form.get("password") == "admin1234":
            session["admin_logged_in"] = True
            return redirect("/topic_admin")
        else:
            return "Wrong password. <a href='/password_admin'>Try again</a>"

    return '''
            <form method="POST">
                Admin Password: <input type="password" name="password"><br>
                <input type="submit" value="Login">
            </form>
            <a href='/topic'>Back</a>
        '''

@app.route("/logout_admin")
def logout_admin():
    session.pop("admin_logged_in", None)
    return redirect("/topic")


@app.route('/easter_egg', methods=['GET','POST'])
def easter_egg():
    if request.method == 'POST':
        facts = [
            "You are doing better than you think.",
            "Every expert was once a beginner.",
            "Flask is cool, and so are you.",
            "One small step today is a big step tomorrow.",
            "You're writing Python like a real developer!"
        ]
        chosen = random.choice(facts)
        return f'''
            <h2>Your random message: </h2>
            <p>{chosen}</p>
            <a href='/easter_egg'>Back</a>
            '''

    return '''
    <form method="POST">
        <input type="submit" value="Get a Random Message">
    </form>
    <br><a href="/">Back</a>
    '''

@app.route('/latest')
def show_latest_message():
    try:
        with open("messages.json", "r", encoding="utf-8") as f:
            all_messages = json.load(f)
            if all_messages:
                last_list = all_messages[-1]
                last_message = (last_list['name'] + ' : ' + last_list['message'])
            else:
                last_message = "(No messages yet.)"
    except FileNotFoundError:
        last_message = "(No messages yet.)"

    return f'''
    <head><title>Latest Message</title></head>
    <h2>Latest message:</h2><p>{last_message}</p><br>
    <a href='/message'>Back to Message Page</a>
    '''

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='localhost', port=9090)

