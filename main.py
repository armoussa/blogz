from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

#displays form and list of todos
@app.route('/', methods=['POST', 'GET'])
def index():

  return redirect("/blog")

@app.route('/blog',methods=['POST','GET']) 
def blog():
    blog_id = request.args.get('id')
    posts = Blog.query.all()

    if blog_id:
        post = Blog.query.filter_by(id=blog_id).first()
        return render_template("solopost.html",title=post.title, body=post.body)


    return render_template('blog.html',posts=posts)


@app.route('/newpost',methods=['POST','GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
   

        title_error = ""
        body_error = ""

        if title == "":
            title_error = "Please enter a title to proceed."
        if body == "":
            body_error = "Please enter some text to proceed."

        if not title_error and not body_error:
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            page_id = new_post.id
            return redirect("/blog?id={0}".format(page_id))
        else:
            return render_template("newpost.html",
                title = title,
                body = body,
                title_error = title_error,
                body_error = body_error
            )
    return render_template("newpost.html")

if __name__ == '__main__':
    app.run()