from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# sets up flask app
app = Flask(__name__)
# sets up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Blog Post:\t{self.id}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET'])
def index2():
    return render_template('home.html')

@app.route('/initposts')
def initposts():
    all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
    all_posts.reverse()
    return render_template('posts.html', posts=all_posts)

@app.route('/addposts')
def addposts():
    post_title = request.args.get('title')
    post_author = request.args.get('author')
    post_content = request.args.get('content')
    new_post = BlogPost(title=post_title,
                        author=post_author,
                        content=post_content)
    db.session.add(new_post)
    db.session.commit()

    all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
    all_posts.reverse()
    return render_template('posts.html', posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete2(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
    all_posts.reverse()
    return render_template('posts.html', posts=all_posts)

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/home')
    else:
        return render_template('edit.html',post=post)
        




#not necessary, but convenient for realtime development
if __name__ == "__main__":
    app.run(debug=True)  #enables changes to take place immediately