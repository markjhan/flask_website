from flask import Flask, render_template, request, json, session, redirect
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = "admin1234"
app.config['admin'] = ""

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
    <!DOCTYPE html>
    <html>
    <head>
        <title>Main Page</title>
        <style>
            body {
                font-family: Arial, sans-serif;     /* Use Arial font; fallback to system default sans-serif */
                max-width: 300px;                   /* Limit page width to 600px for better readability */
                margin: auto;                       /* Center the content horizontally */
                padding: 40px;                      /* Add 40px space around the content */
                background-color: #E0F8F7;          /* Set a background color */
            }
            h1 {
                color: #333333;                        /* Set color for the main heading */
            }
            a {
                display: block;                     /* Make each link appear on its own line */
                margin: 6px 0;                     /* Add vertical spacing between links */
                font-size: 21px;                    /* Set link text size */
                text-decoration: none;              /* Remove the underline from links */
                color: #1E90FF;                     /* Set link color */
            }
            a:hover {
                color: #104E8B;                     /* Change link color when hovered */
            }
            .admin {
                margin-top: 40px;                   /* Add top margin above admin section */
                font-weight: bold;                  /* Make admin link text bold */
                font-size: 20px;
                color: #FF0000;                     /* Set color */
                border: 2px solid red;         /* Add a solid red border */
                padding: 8px 16px;             /* Add spacing inside the button */
                display: inline-block;         /* Allow sizing and box styling */
                border-radius: 6px;            /* Round the corners */
                text-align: center;            /* Center the text */
                background-color: white;       /* Set background color */
                text-decoration: none;         /* Remove underline from link */
            }
            .admin:hover {
                background-color: #ffe6e6;     /* Light red background on hover */
                color: darkred;                /* Change text color on hover */
                border-color: darkred;         /* Change border color on hover */
            }
        </style>
    </head>
    <body>
        <h1>
            Main Page<br><br>
            <a href="/about">Go to About Page </a><br>
            <a href="/message">Go to Message Page</a><br>
            <a href="/search">Go to Search Page</a><br>
            <a href="/easter_egg">Get a surprise</a><br>
            <br><br>
            <a href="/admin" class="admin">Admin Page</a><br>
        </h1>
    </body>
    </html>
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
            },
            {
                'title': 'Admin',
                'url': '/admin',
                'content': 'Admin Page to Manage messages and topics.'
            },
            {
                'title': 'Topic',
                'url': '/topic',
                'content': 'Leave messages with topics, see and search topic messages.'
            }
        ]

        if msg:
            for result in search_index:
                combined_text = (result['title'] + ' ' + result['content']).lower()
                if msg in combined_text:
                    matches.append(result)

            html = ""

            for match in matches:
                html += f"<p><a href={match['url']}>{match['title']}</a></p>"

            if html:
                return f'''
                    <head>
                        <link rel="stylesheet" href="/static/style_standard_background.css">
                    </head>
                    <h2>Search Results:</h2><br>
                    {html}<br><br>
                    <h3><a href='/search'>Back</a></h3>
                    '''
            else:
                return '''
                    <head>
                        <link rel="stylesheet" href="/static/style_standard_background.css">
                    </head>
                    <h2>No results found</h2><br><br>
                    <h3><a href='/search'>Back</a></h3>
                    '''
        else:
            return '''
                <head>
                    <link rel="stylesheet" href="/static/style_simple_background_only.css">
                    <style>
                        body {
                            max-width: 800px;
                            padding: 40px;
                        }
                        .link-container {
                            text-align: center;
                        }
                        .link-container a {
                            font-size: 30px;
                            color: #1E90FF;
                            display: inline-block;
                            text-decoration: none;
                        }
                        .link-container a:hover {
                            color: #10418B;
                        }
                    </style>
                </head>
                <h1>
                    Please enter the information you want to search<br><br>
                    <div class="link-container">
                        <a href="/search">Back</a>
                    </div>
                </h1>
            '''

    return ''' 
        <head>
            <link rel="stylesheet" href="/static/style_standard_background.css">
            <link rel="stylesheet" href="/static/style_input_blank.css">
        </head>    
        <h1>Search Something</h1>
        <form method="POST">
            Search: <br>
            <textarea name="search" rows="4" cols="40"></textarea><br><br>

            <input type="submit" value="Search">
        </form>
        <br>
        <a href='/'>Back to Main Page</a>
        '''

@app.route('/secret')
def secret():
    return render_template("secret.html")

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
                    <head>
                    <link rel="stylesheet" href="/static/style_standard_background.css">
                    <style>
                        p {
                            font-size: 20px;
                        }
                    </style>
                    </head>
                    <p>No message found for this code.</p><br>
                    <a href='/get_message'>Back</a>
                    '''

            result_html += "<a href='/get_message'>Back</a>"
            return f'''
                <head>
                    <link rel="stylesheet" href="/static/style_standard_background.css">
                    <style>
                        p {{
                            font-size: 20px;
                        }}
                    </style>
                </head>
                {result_html}
                '''
        else:
            return '''
                <head>
                    <link rel="stylesheet" href="/static/style_standard_background.css">
                    <style>
                        p {
                            font-size: 20px;
                        }
                    </style>
                </head>
                <p>Please enter a code.</p><br>
                <a href='/get_message'>Back</a>
                '''

    return '''
    <head>
        <title>Get</title>
        <link rel="stylesheet" href="/static/style_standard_background.css">
        <link rel="stylesheet" href="/static/style_input_blank.css">
    </head>
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
                    return f'''
                        <head>
                            <link rel="stylesheet" href="/static/style_standard_background.css">
                        </head>
                        {html}
                        '''

                else:
                    return '''
                        <head>
                            <link rel="stylesheet" href="/static/style_standard_background.css">
                        </head>
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
                <head>
                    <link rel="stylesheet" href="/static/style_standard_background.css">
                </head>
                <h2>Please enter a name.</h2>
                <br><a href='/search_by_name'>Back</a>
                '''

    return '''
    <head>
        <link rel="stylesheet" href="/static/style_standard_background.css">
        <link rel="stylesheet" href="/static/style_input_blank.css">
        <style>
            p {
                font-size: 20px;
            }
        </style>
    </head>
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
    return render_template("about.html")

@app.route('/message', methods=['GET','POST'])
def message():
    if request.method == 'POST':
        name = request.form.get('name')
        msg = request.form.get('message')
        is_secret = request.form.get('is_secret')
        is_topic = request.form.get('is_topic')

        if name and msg:
            if is_secret:
                code = request.form.get('code')
                if code:
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

                    return f'''
                        <head>
                            <link rel="stylesheet" href="/static/style_standard_background.css">
                            <style>
                                p {{
                                    font-size: 26px;
                                    padding: 80px;
                                }}
                            </style>
                        </head>
                        <body>
                            <p>Thank you for your secret, {name}! <br><br><br><br><a href='/message'>Back to Message Page</a></p>
                        </body>
                        '''
                else:
                    return '''
                        <head>
                            <link rel="stylesheet" href="/static/style_only_words.css">
                        </head>
                        <body>
                            <p>Please enter a code.</p>
                            <a href="/message">Back</a>
                        </body>
                    '''

            elif is_topic:
                topics = request.form.get('topic')

                if topics:
                    print(f"Receive：{name} - {msg} - {topics}")

                    new_entry = {
                        "name": name,
                        "message": msg,
                        "topic": topics,
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }

                    try:
                        with open("messages_topic.json", "r", encoding="utf_8") as f:
                            all_messages = json.load(f)
                    except FileNotFoundError:
                        all_messages = []

                    all_messages.append(new_entry)

                    with open("messages_topic.json", "w", encoding="utf-8") as f:
                        json.dump(all_messages, f, indent=2, ensure_ascii=False)

                    return """
                        <head>
                            <link rel="stylesheet" href="/static/style_only_words.css">
                        </head>
                        <body>
                            <h2>Topic Message Received!</h2><br>
                            <a href='/message'>Back</a>
                        </body>
                    """
                else:
                    return '''
                        <head>
                            <link rel="stylesheet" href="/static/style_only_words.css">
                        </head>
                        <body>
                            <h2>Please enter a topic.</h2><br>
                            <a href='/message'>Back</a>
                        </body>
                    '''

            else:
                print(f"Receive：{name} - {msg}")  # To confirm receive the message or not

                label, reply = analyze_message(msg)

                new_entry = {
                    "name": name,
                    "message": msg,
                    "label": label,
                    "reply": reply,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M")
                }

                try:
                    with open("messages.json", "r", encoding="utf_8") as f:
                        all_messages = json.load(f)
                except FileNotFoundError:
                    all_messages = []

                all_messages.append(new_entry)

                with open("messages.json", "w", encoding="utf-8") as f:
                    json.dump(all_messages, f, indent=2, ensure_ascii=False)

                return f"""
                        <head>
                            <link rel="stylesheet" href="/static/style.css">
                            <style>
                                body {{
                                    max-width: 800px;
                                    padding: 40px;
                                    text-align: center;
                                }}
                                p {{
                                    font-size: 18px;
                                }}
                                a {{
                                    font-size: 18px;
                                }}
                            </style>
                        </head>
                        <body>
                            <h2>Message received!</h2><br>
                            <p><strong>You said: </strong>{msg}</p>
                            <p><strong>Bot replied: </strong>{reply}</p>
                            <a href='/message'>Back</a>
                        </body>
                        """

        else:
            return '''
                    <head>
                        <link rel="stylesheet" href="/static/style.css">
                        <style>
                            body {
                                max-width: 500px;
                                padding: 40px;
                                text-align: center;
                            }
                            a {
                                font-size: 20px;
                            }
                        </style>
                    </head>
                    <body>
                        <h2>Please enter your name and message.</h2><br>
                        <a href='/message'>Back</a>
                    </body>
                    '''

    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Message Board</title>
        <link rel="stylesheet" href="/static/style_simple_background_only.css">
        <link rel="stylesheet" href="/static/style_input_blank.css">
        <style>
            body {
                max-width: 300px;
                padding: 40px;
            }
            h1 {
                color: #121212;
            }
            a {
                margin: 0px 0;
                font-size: 16px;
                color: #1E90FF;
            }
            a:hover {
                color: #10418B;
            }
            .link-container {
                text-align: center;
            }
            .link-container a {
                font-size: 17px;
                color: #1E90FF;
                display: block;
                text-decoration: none;
            }
            .link-container a:hover {
                color: #10418B;
            }

        </style>
    </head>
    
    <body>
        <h1>Message Board</h1>
        <form method="POST">
            Your Name:<br>
            <input type="text" name="name"><br><br>
    
            Message:<br>
            <textarea name="message" rows="4" cols="40"></textarea><br><br>
            
            <input type="checkbox" id="secret" name="is_secret" onclick="updateFields('secret')">
            Send as <a href="/secret">Secret Message</a>?<br><br>
            
            <div id="codeField" style="display: none; margin-top: 10px;">
                <label for="secret_code">Code:</label>
                <input type="text" id="secret_code" name="code">
            </div>
            
            <input type="checkbox" id="topic" name="is_topic" onclick="updateFields('topic')">
            Send as a Topic Message?<br><br>
            
            <div id="topicField" style="display: none; margin-top: 10px;">
                <label for="topic_input">Topic:</label>
                <input type="text" id="topic_input" name="topic">
            </div>
    
            <input type="submit" value="Submit">
        </form>
        
        <br><br><br><br><br><br><br><br>
        <div class="link-container">
            <a href="/">Back to Main Page</a><br>
            <a href="/latest">Check the latest message</a><br>
            <a href='/get_message'>Get Messages by Code</a><br>
            <a href='/search_by_name'>Search Messages by name</a><br>
            <a href='/topic_view'>View and Search Messages with Topic</a><br>
        </div>
        
        <script>
            function updateFields(selected) {
                const secretCheckbox = document.getElementById('secret');
                const codeField = document.getElementById('codeField');
                const topicCheckbox = document.getElementById('topic');
                const topicField = document.getElementById('topicField');
                
                if (selected === 'secret') {
                    document.getElementById('topic').checked = false;
                } else if (selected === 'topic') {
                    document.getElementById('secret').checked = false;
                }
                
                if (secretCheckbox.checked) {
                    codeField.style.display = 'block';
                } else {
                    codeField.style.display = 'none'; 
                }
                
                if (topicCheckbox.checked) {
                    topicField.style.display = 'block';
                } else {
                    topicField.style.display = 'none'; 
                }
            }
        </script>
    </body>
    </html>
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
                        html += f"<p><strong>{match['topic']}</strong> -- {match['message']} -- {match['time']}</p>"
                    html += "<br><br><a href='/topic_view'>Back</a>"
                    return f'''
                        <head>
                            <link rel="stylesheet" href="/static/style_standard_background.css">
                        </head>
                        <body>
                            {html}
                        </body>
                    '''

                else:
                    return '''
                        <head>
                            <link rel="stylesheet" href="/static/style_only_words.css">
                        </head>
                        <body>
                            <h2>No messages found for this topic.</h2>
                            <br><a href='/topic_view'>Back</a>
                        </body>
                        '''
            except FileNotFoundError:
                return '''
                        <h2>No message data found.</h2>
                        <br><a href='/topic'>Back</a>
                        '''
        else:
            return '''
                <head>
                    <link rel="stylesheet" href="/static/style_only_words.css">
                </head>
                <body>
                    <h2>Please enter a topic.</h2>
                    <br><a href='/topic_view'>Back</a>
                </body>
                '''

    msgs = []
    try:
        with open("messages_topic.json", "r", encoding="utf-8") as f:
            all_messages = json.load(f)
        for result in all_messages:
            msg = (result['message'] + ' -- ' + result['time'])
            msgs.append(msg)
    except FileNotFoundError:
        msgs = "(No messages yet.)"
    msg_html = "<br>".join(msgs)

    return f'''
        <head>
            <link rel="stylesheet" href="/static/style_standard_background.css">
            <link rel="stylesheet" href="/static/style_input_blank.css">
        </head>
        <body>
            <h1>Enter a Topic</h1>
            <h2>
            <form method="POST">
                Topic: <br>
                <input type="text" name="search topic"><br><br>
    
                <input type="submit" value="Submit">
            </form>
            <a href="/message">Back</a><br><br><br><br>
            </h2>
            {msg_html}<br>
        </body>
        '''

@app.route("/admin")
def admin():
    app.config['admin'] = ''
    if not session.get("admin_logged_in"):
        return redirect("/password_admin")

    return '''
    <head>
        <link rel="stylesheet" href="/static/style_admin.css">
        <style>
            a {
                font-size: 30px;
            }
            h1 {
                color: #FFFFFF;
            }
        </style>
    </head>
    <body>
        <h1>Welcome Admin!<br><br>
        <a href="/topic_admin">Managing Topic Messages</a><br><br>
        <a href="/normal_admin">Managing Normal Messages</a><br><br>
        <a href="/logout_admin">Logout Out</a><br><br>
        </h1>
    </body>
    '''

@app.route('/normal_admin')
def normal_admin():
    if not session.get("admin_logged_in"):
        return redirect("/password_admin")

    app.config['admin'] = "normal"
    with open("messages.json", "r", encoding="utf-8") as f:
        all_messages = json.load(f)

    html = "<h1>Admin Panel: Manage Messages</h1>"
    html += "<a href='/admin'>Back</a><br><br><br>"
    for idx, msg in enumerate(all_messages):
        html += f'''
            <div style="display: flex; justify-content: center;">
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <p><span><strong>{msg['name']}</strong>: {msg['message']} -- {msg['time']}</span>
                    <form method="POST" action="/delete/{idx}" style="margin-left: 25px;">
                        <input type="submit" value="Delete">
                    </form></p>
                </div>
            </div>
        '''
    return f'''
        <head>
            <link rel="stylesheet" href="/static/style_admin.css">
            <link rel="stylesheet" href="/static/style_admin_delete_button.css">
            <style>
                a {{
                    font-size: 27px;
                }}
                p {{
                    font-size: 18px;
                    color: #FFFFFF;
                }}
                h1 {{
                    color: #FFFFFF;
                }}
            </style>
        </head>
        <body>
           {html}
        </body>
    '''

@app.route('/topic_admin')
def topic_admin():
    if not session.get("admin_logged_in"):
        return redirect("/password_admin")

    app.config['admin'] = "topic"
    with open("messages_topic.json", "r", encoding="utf-8") as f:
        all_messages = json.load(f)

    html = "<h1>Admin Panel: Manage Topic Messages</h1>"
    html += "<a href='/admin'>Back</a><br><br><br>"
    for idx, msg in enumerate(all_messages):
        html += f'''
            <div style="display: flex; justify-content: center;">
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <p><span><strong>{msg['name']}</strong>: {msg['message']} -- {msg['topic']} -- {msg['time']}</span>
                    <form method="POST" action="/delete/{idx}" style="margin-left: 25px;">
                        <input type="submit" value="Delete">
                    </form></p>
                </div>
            </div>
        '''
    return f'''
        <head>
            <link rel="stylesheet" href="/static/style_admin.css">
            <link rel="stylesheet" href="/static/style_admin_delete_button.css">
            <style>
                a {{
                    font-size: 27px;
                }}
                p {{
                    font-size: 18px;
                    color: #FFFFFF;
                }}
                h1 {{
                    color: #FFFFFF;
                }}
            </style>
        </head>
        <body>
            {html}
        </body>
    '''

@app.route("/delete/<int:idx>", methods=["POST"])
def delete_message(idx):
    if not session.get("admin_logged_in"):
        return redirect("/password_admin")

    if app.config['admin'] == "normal":
        try:
            with open("messages.json", "r", encoding="utf-8") as f:
                all_messages = json.load(f)

            if 0 <= idx < len(all_messages):
                all_messages.pop(idx)

            with open("messages.json", "w", encoding="utf-8") as f:
                json.dump(all_messages, f, indent=2, ensure_ascii=False)

        except FileNotFoundError:
            pass

        return redirect("/normal_admin")

    elif app.config['admin'] == "topic":
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
            return redirect("/admin")
        else:
            return '''
                <head>
                    <link rel="stylesheet" href="/static/style_standard_background.css">
                </head>
                <body>
                    Wrong password. <a href='/password_admin'>Try again</a>
                </body>
            '''

    return '''
        <head>
            <link rel="stylesheet" href="/static/style_standard_background.css">
        </head>
        <body>
            <form method="POST">
                Admin Password: <input type="password" name="password"><br><br>
                <input type="submit" value="Login">
            </form>
            <a href='/'>Back</a>
        </body>
    '''

@app.route("/logout_admin")
def logout_admin():
    session.pop("admin_logged_in", None)
    return redirect("/")

@app.route('/easter_egg', methods=['GET','POST'])
def easter_egg():
    if request.method == 'POST':
        facts = [
            "You are doing better than you think.",
            "Every expert was once a beginner.",
            "Flask is cool, and so are you.",
            "One small step today is a big step tomorrow.",
            "You're writing Python like a real developer!",
            "No matter where you start, you can build something amazing.",
            "This little site proves that learning by doing works — you can do it too.",
            "You don’t need permission to learn. Just start.",
            "This project began with zero experience. Yours can too.",
            "If you're curious enough to click this, you're curious enough to create.",
            "You don't need a classroom to build something real.",
            "One line of code at a time — that’s how anything starts.",
            "Everyone begins somewhere. This is a somewhere.",
            "The person who built this site used to know nothing about Flask — and now look."
        ]
        chosen = random.choice(facts)
        return render_template("easter_egg.html", message=chosen)

    return render_template("easter_egg.html")

@app.route('/latest')
def show_latest_message():
    try:
        with open("messages.json", "r", encoding="utf-8") as f:
            all_messages = json.load(f)
            if all_messages:
                last_list = all_messages[-1]
                last_message = (last_list['name'] + ' : ' + last_list['message'] + ' -- ' + last_list['time'])
            else:
                last_message = "(No messages yet.)"
    except FileNotFoundError:
        last_message = "(No messages yet.)"

    return f'''
    <head>
        <title>Latest Message</title>
        <link rel="stylesheet" href="/static/style_standard_background.css">
        <style>
            p {{
                font-size: 18px;
            }}
        </style>
    </head>
    <h2>Latest message:</h2><p>{last_message}</p><br>
    <a href='/message'>Back to Message Page</a>
    '''

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='localhost', port=9090)

