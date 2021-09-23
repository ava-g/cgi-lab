#!/usr/bin/env python3
import os, json
import cgi
import cgitb
import login
import secret
from http.cookies import SimpleCookie

# from templates.py
def login_page():
    """
    Returns the HTML for the login page.
    """

    return _wrapper(r"""
    <h1> Welcome! </h1>

    <form method="POST" action="login.py">
        <label> <span>Username:</span> <input autofocus type="text" name="username"></label> <br>
        <label> <span>Password:</span> <input type="password" name="password"></label>

        <button type="submit"> Login! </button>
    </form>
    """)

def after_login_incorrect():
    """
    Returns the HTML for the page when the login credentials were typed
    incorrectly.
    """
    return _wrapper(r"""
    <h1> Login incorrect :c </h1>

    <p> Incorrect username or password (hint: <span class="spoilers"> Check
        <code>secret.py</code>!</span>)
    <p> <a href="login.py"> Try again. </a>
    """)

# from template.py
def secret_page(username=None, password=None):
    """
    Returns the HTML for the page visited after the user has logged-in.
    """
    if username is None or password is None:
        raise ValueError("You need to pass both username and password!")

    return _wrapper("""
    <h1> Welcome, {username}! </h1>

    <p> <small> Pst! I know your password is
        <span class="spoilers"> {password}</span>.
        </small>
    </p>
    """.format(username=escape(username.capitalize()),
               password=escape(password)))

def _wrapper(page):
    """
    Wraps some text in common HTML.
    """
    return ("""
    <!DOCTYPE HTML>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                max-width: 24em;
                margin: auto;
                color: #333;
                background-color: #fdfdfd
            }

            .spoilers {
                color: rgba(0,0,0,0); border-bottom: 1px dashed #ccc
            }
            .spoilers:hover {
                transition: color 250ms;
                color: rgba(36, 36, 36, 1)
            }

            label {
                display: flex;
                flex-direction: row;
            }

            label > span {
                flex: 0;
            }

            label> input {
                flex: 1;
            }

            button {
                font-size: larger;
                float: right;
                margin-top: 6px;
            }
        </style>
    </head>
    <body>
    """ + page + """
    </body>
    </html>
    """)

def main():
    '''
    print("Content-type:text/html\r\n\r\n")
    print("<title>Test CGI</title>")
    print("<p>Hello World from cmput404!</p>")

    print(os.environ)
    '''
    json_object = json.dumps(dict(os.environ), indent = 4)
    #print(json_object)
    '''
    for param in os.environ.keys():
        if (param == "QUERY_STRING"):
            print("<b>%20s<b>: %s<br>" % (param, os.environ[param]))

    for param in os.environ.keys():
        if (param == "HTTP_USER_AGENT"):
            print("<b>%20s<b>: %s<br>" % (param, os.environ[param]))
    '''
    #print(login_page())
    login.login()

    cookie_data = dict(os.environ)["HTTP_COOKIE"]
    cookies = SimpleCookie()
    cookies.load(cookie_data)
    cookie_dict = {}
    for key, value in cookies.items():
        cookie_dict[key] = value.value

    if ("password" in cookie_dict and "username" in cookie_dict):
        if (cookie_dict["password"] == secret.password and cookie_dict["username"] == secret.username):
            print(secret_page(cookie_dict["username"]), cookie_dict["password"])
        else:  # login fails
            print(after_login_incorrect())
    else:
        print(login_page())

if __name__ == "__main__":
    main()
