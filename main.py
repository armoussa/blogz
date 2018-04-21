from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:launchcode@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')


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


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        user_error = ""
        pass_error = ""

        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        if not user:
            user_error = "Username does not exist."
            return(render_template('login.html',user_error=user_error)

            #flash('User password incorrect, or user does not exist', 'error')
        else:
            pass_error = "Your username or password was incorrect."
            return(render_template('login.html',pass_error=pass_error)
            # username or password is incorrect    

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        user_error = ""
        pass_error = ""
        verify_error = ""

        # TODO - validate user's data


        if username == "":
            user_error = "Please enter a valid username."

        elif len(username) < 3:
            user_error = "Username invalid. Please enter a username greater than 3 characters."

        if password == "":
            pass_error = "Please enter a valid password."

        elif len(password) < 3:
            pass_error = "Password invalid. Please enter a password greater than 3 characters."

        if password != verify or verify != password:
            verify_error = "Passwords do not match. Please try again."

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            user_error = "Username already taken. Please choose a new username."

        if len(username) > 3 and len(password) > 3 and password==verify and not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        else:
            # TODO - user better response messaging
            return render_template('signup.html',
            username = username, user_error=user_error,
            pass_error=pass_error,verify_error=verify_error)

    return render_template('signup.html')


@app.route('/newpost',methods=['POST','GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()

        title_error = ""
        body_error = ""

        if title == "":
            title_error = "Please enter a title to proceed."
        if body == "":
            body_error = "Please enter some text to proceed."

        if not title_error and not body_error:
            new_post = Blog(title, body, owner)
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