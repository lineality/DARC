from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

# this is the database
# to create the database directory, go into a python env
# run
# >>> from app import db
# >>> db.create_all()
# >>> from app import Blogpost

class BlogPost(db.Model):
    # add nouns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    #nouns = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    #character_actions = db.relationship('CharacterActions', backref='blogpost', lazy=True)
    def __repr__(self):
        return 'Blog post ' + str(self.id)

class CharacterActions(db.Model):
    # add dice rolls
    # add nouns
    id = db.Column(db.Integer, primary_key=True)
    #nouns = db.Column(db.String(100), nullable=False)
    action = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    #dicerolls = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #blogpost_id = db.Column(db.Integer, db.ForeignKey('blogpost.id'), nullable=False)
    def __repr__(self):
        return 'Character Actions ' + str(self.id)

# Root rout
@app.route('/')
#this takes HTML
def index():
    return render_template('index.html')

#making sure posting is allowed (get only is default)
@app.route('/posts', methods=['GET', 'POST'])
def posts():

    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)

    # defining a variable 
    #return render_template('posts.html', posts=all_posts)

# this shuld be a page where players read scenes and contact DM
@app.route('/game', methods=['GET', 'POST'])
def game():

    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('game.html', posts=all_posts)

    # defining a variable 
    #return render_template('game.html', posts=all_posts)

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

@app.route('/posts/characteractions/<int:id>', methods=['GET', 'POST'])
def character_actions(id):

    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('characteractions.html', post=post)

@app.route('/posts/newscene', methods=['GET', 'POST'])
def new_scene():
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_scene.html')

if __name__ == "__main__":
    app.run(debug=True)