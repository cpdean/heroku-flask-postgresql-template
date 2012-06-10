#!/usr/bin/python
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from werkzeug import secure_filename
import os


app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['jpg'])

import db


@app.route('/')
def index():
    return redirect(url_for("post_list"))

@app.route('/posts/',methods=['POST','GET'])
def post_list():
    if request.method == 'POST':
        p = db.Post()
        p.title = request.form['title']
        p.caption = request.form['caption']
        i_data = get_image(request)
        p.image_data = i_data if i_data is not None else ''
        p.save()
        return redirect(url_for("post_list"))

    elif request.method == 'GET':
        posts = db.Post().show()
        return render_template("posts.html", posts=posts )

#FILE HANDLING

def allowed_file(filename):
    return '.' in filename and\
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_image(r):
    image = r.files['file']
    if image and allowed_file(image.filename):
        return image.read()

@app.route('/post/',methods=['POST','GET'])
def redirect_to_latest():
    return redirect(url_for("show_latest_post"))

@app.route('/post/latest',methods=['POST','GET'])
def show_latest_post():
    post = db.get_latest_post()
    return render_template("view_post.html", post=post )

@app.route('/post/<int:post_id>',methods=['POST','GET'])
def show_post(post_id=None):
    if request.method == 'POST':
        pass

    elif request.method == 'GET':
        post = db.Post(post_id)
        return render_template("view_post.html", post=post )


if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.debug = True if port == 5000 else False
    app.run(host="0.0.0.0",port=port)
