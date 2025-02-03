from flask import Flask
import os

app = Flask(_name_)

@app.route('/')
def hello():
    return "Hello, World!"

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))