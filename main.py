from flask import Flask, request, redirect, render_template, flash, session 
from flask_sqlalchemy import SQLAlchemy 
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Blogz4LC101@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True 
db = SQLAlchemy(app)
app.secret_key = '3p89bj23089uv023@)(*%'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(1500))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, title, body, author):
        self.title = title
        self.body = body
        self.author = author

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(100))
    blogs = db.relationship('Blog', backref = 'author')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    # def __repr__(self):
        # return '<User %r>' % self.email

@app.before_request
def require_login():
#    if 'email' not in session:
#        redirect('/login')
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if 'email' in session:
        del session['email']
    # return render_template('signup.html')

    if request.method =='POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        
        name_error = ''
        pw_error = ''
        verify_error = ''
        email_fail = ''

        if len(name) < 2 or len(name) > 60:
            name_error = "Schucks... Username not valid."
            name = ''
        #elif ' ' in username:
            #un_error = "Remove spaces from your username!"
            #username = ''
                    
        if len(password) == 0:
            pw_error = 'You need to add a password.'

        elif len(password) < 3 or len(password) > 20:
            pw_error = 'Please enter a valid password'

        if verify != password:
            verify_error = 'These passwords do not match. Make them the same, and write them down somewhere so you do not forget'

        if len(email) > 0:
            if not is_email(email):
                email_fail = 'Rut-Roh... ' + email + ' might not be a "REAL" email address!'
                email = ''

        if  (name_error or
                pw_error or
                verify_error or
                email_fail):
            #return render_template('blog.html', username=username)
            # return redirect('/')
            return render_template('signup.html', email=email, name_error=name_error, pw_error=pw_error, verify_error=verify_error, email_fail=email_fail)
    
        existing = User.query.filter_by(email=email).first()
        if not existing:
            new_user = User(name, email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            flash('Logged In')
            # return redirect('/blog?id=' + str(new_user.name))
            return render_template('singleuser.html', email=email, user=new_user)
        else: 
            flash('Duplicate User Attempt, please login!', 'error')

    return render_template('signup.html', title = "Blogz New User")        

def is_email(string):

    atsign_index = string.find('@')
    atsign_present = atsign_index >= 0
    if not atsign_present:
        return False
    else:
        domain_dot_index = string.find('.', atsign_index)
        domain_dot_present = domain_dot_index >= 0
        return domain_dot_present


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form ['password']
        user = User.query.filter_by(email=email).first()
        
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            print(session)
            blogs = Blog.query.filter_by(author_id = user.id).all()
            
            return render_template('singleuser.html', email=email, user=user, blogs=blogs)
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

    #error = ''
    #if request.method == 'GET':
        #return render_template('login.html', title = "Login to Blogz")


@app.route("/blog", methods=['POST', 'GET'])
def blog():
    users = User.query.all()
    if request.args.get('id') != None:
        blog_id =  request.args.get('id')
        blog = Blog.query.filter_by(id = blog_id).first()
        print(blog.author_id)
        print("Individual Route")

        user = User.query.filter_by(id = blog.author_id).first()
        return render_template('indiv_entry.html', title = "Read a Single entry", blog=blog, user = user)            
   
    elif request.args.get("userid") != None:
        owner_id =  request.args.get('userid')
        blogs = Blog.query.filter_by(author_id = owner_id).all()
        return render_template('blog.html', title = 'Blogs by specific owner', blogs=blogs, users=users)

        

    else:
        blogs = Blog.query.all()
        users = User.query.all()
        return render_template('blog.html', title = "Read Whatcha Wrote", blogs=blogs, users=users)
        
        

@app.route("/newpost", methods=['POST', 'GET'])
def newpost():
    error = ''
    author = User.query.filter_by(email=session['email']).first()
    if request.method == 'GET':
        return render_template('newpost.html', title = "Add more memories!", user=author)

    if request.method == 'POST':
        post_title = request.form['blog_title']
        post_body = request.form['blog_body']
        

        if len(post_title) == 0 or len(post_body) == 0:
            error = "Make sure title and body are filled in."
            return render_template('newpost.html', title = "Add more memories!", error=error, user=author)
        else:
            new_entry = Blog(post_title, post_body, author)
            db.session.add(new_entry)
            db.session.commit()

            blogs = Blog.query.all()    
            return redirect('/blog?id=' + str(new_entry.id)) 
            #return redirect('/blog')

    else:
        return redirect('/')

   

    
@app.route("/logout")
def logout():
    # if request.method == 'GET':
        #return render_template('login.html', title = "Buh-Bye!")

    if 'email' in session:
        del session['email']
    return redirect('/login')

@app.route("/", methods=['POST', 'GET'])
def index():
    author = User.query.filter_by(email=session['email']).first()
    users = User.query.all()
    if request.method == 'POST':
        post_title = request.form['blog_title']
        post_body = request.form['blog_body']

        new_entry = Blog(post_title, post_body, author)
        db.session.add(new_entry)
        db.session.commit()
    
    blogs = Blog.query.filter_by(author=author).all()
    return render_template('index.html', title = "All my Blogz", blogs=blogs, users=users)

    #return render_template('index.html')
    #return redirect('/login')
   




if __name__ == '__main__':
    app.run()

