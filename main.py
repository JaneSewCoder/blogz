from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog-LC101!@localhost:8889/build-a-blog'
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
    return redirect('/blog')



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

   
    
    
if __name__ == '__main__':
    app.run()

