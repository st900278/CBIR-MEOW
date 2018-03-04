import os
from bottle import *
import subprocess
@get('/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='static/js')

@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='static/css')

@get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='.')

@get('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    return static_file(filename, root='static/fonts')

@route('/')
def root():
    return template('index.html', show=[])

@route('/upload', method='POST')
def do_upload():
    category = request.forms.name
    data = request.files.data
    t = []
    if category and data:
        name, ext = os.path.splitext(data.filename)
        if ext not in ('.png', '.jpg', '.jpeg'):
            return "File extension not allowed."

        save_path = "/tmp/{category}".format(category=category)
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        file_path = "{path}/{file}".format(path=save_path, file=data.filename)
        if os.path.isfile(file_path): os.remove(file_path)
        data.save(file_path)
        p = subprocess.Popen(["python", "../multimedia/cbir1.py", "/tmp/meow/"+data.filename], stdout=subprocess.PIPE)
        x = p.stdout.read()
        x = x.split("\n")
        t = []
        for y in x:
            d = y.split("'")
            if len(d) >= 3:
                t.append(d[1])
    
    print t
    return template('index.html', show=t)

if __name__ == '__main__':
    run(host='localhost', port=8080)
