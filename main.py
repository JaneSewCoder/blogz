from flask import Flask, request, redirect, render_template, flash
import cgi
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Blogz4LC101@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True 
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(1500))


    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route("/", methods=['POST', 'GET'])
def index():
    #return render_template('index.html')
    return redirect('/signup')

@app.route("/signup", methods=['GET', 'POST'])


def signup():

    if request.method == 'GET':
        return render_template('signup.html', title = "Blogz New User")

    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        email = request.form['email']
        
        un_error = ''
        pw_error = ''
        verify_error = ''
        email_fail = ''

    if len(username) < 3 or len(username) > 20:
        un_error = "Oopsies!  Please enter a valid username."
        username = ''
    elif ' ' in username:
        un_error = "Remove spaces from your username!"
        username = ''
      
            
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

    if not (un_error or
            pw_error or
            verify_error or
            email_fail):
        #return render_template('blog.html', username=username)
        return redirect('/blog')
    else:
        return render_template('signup.html', username=username, email=email, un_error=un_error, pw_error=pw_error, verify_error=verify_error, email_fail=email_fail)
        

def is_email(string):

    atsign_index = string.find('@')
    atsign_present = atsign_index >= 0
    if not atsign_present:
        return False
    else:
        domain_dot_index = string.find('.', atsign_index)
        domain_dot_present = domain_dot_index >= 0
        return domain_dot_present


@app.route("/blog", methods=['POST', 'GET'])
def blog():

    

    if request.args.get('id'):
        blog_id =  request.args.get('id')
        blog = Blog.query.filter_by(id = blog_id).first()
        return render_template('indiv_entry.html', title = "Read a Single entry", blog=blog)            

    else:
        blogs = Blog.query.all()
        return render_template('blog.html', title = "Read Whatcha Wrote", blogs=blogs)
        
        

@app.route("/newpost", methods=['POST', 'GET'])
def newpost():
    error = ''
    if request.method == 'GET':
        return render_template('newpost.html', title = "Add more memories!")

    if request.method == 'POST':
        post_title = request.form['blog_title']
        post_body = request.form['blog_body']

        if len(post_title) == 0 or len(post_body) == 0:
            error = "Make sure title and body are filled in."
            return render_template('newpost.html', title = "Add more memories!", error=error)
        else:
            new_entry = Blog(post_title, post_body)
            db.session.add(new_entry)
            db.session.commit()

            blogs = Blog.query.all()    
            return redirect('/blog?id=' + str(new_entry.id)) 
            #return redirect('/blog')

    else:
        return redirect('/')

   
@app.route("/login", methods=['POST', 'GET'])
def login():
    error = ''
    if request.method == 'GET':
        return render_template('login.html', title = "Login to Blogz")

    
@app.route("/logout", methods=['POST', 'GET'])
def logout():
    error = ''
    if request.method == 'GET':
        return render_template('login.html', title = "Buh-Bye!")

if __name__ == '__main__':
    app.run()

