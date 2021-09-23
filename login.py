#!/usr/bin/env python3
import cgi, cgitb
import secret

def login():
    print("Content-type:text/html\r\n\r\n")

    # create instance of FieldStorage
    form = cgi.FieldStorage()
    # get data from fields
    username = form.getvalue("username")
    pwd = form.getvalue("password")

    if username == secret.username and pwd == secret.password:
        print("Set-Cookie:username = ", username, "\r\n")
        print("Set-Cookie:password = ", pwd, "\r\n")
