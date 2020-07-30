from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title =  db.Column(db.String(100), nullable =False)  # nullable is false thus it means it has to be here.
    content = db. Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable = False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog Post' + str(self.id)


"""all_posts = [
    {
        'title':'Post 1',
        'content':'This is the content of post 1...',
        'author':'Kritika'
    },
    {
        'title':'Post 2',
        'content':'This is the content of post 2...'
    }
]"""

# routing
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_author = request.form['author']
        post_content = request.form['content']
        new_post= BlogPost(title=post_title, content=post_content, author=post_author)  #author='Kritika'
        db.session.add(new_post)
        db.session.commit()  # to save it permanently
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)    


"""@app.route('/home')
def hello():
    return "Hello World"


@app.route('/new')
def new():
    return 'new page'

@app.route('/profile/<name>')
def profile(name):
    return 'This profile belongs to %s.' %name


@app.route('/profile/<int:id>')
def profiles(id):
    return 'This profile belongs to %d.' %id

@app.route('/home/<string:name>')
def hello(name):
    return "Hello, " + name


@app.route('/home/<int:id>')
def hello_(id):
    return "Hello, " + str(id)   """


@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
        
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():

    if request.method == 'POST':
        
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        new_post= BlogPost(title=post_title, content=post_content, author=post_author)  #author='Kritika'
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')



# does not give 404 error on some mistakes.
if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
