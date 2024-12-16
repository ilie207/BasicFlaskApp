from flask import Flask, render_template, request, redirect, url_for
from models import BlogPost, db
from statistics import median, mean
app = Flask(__name__)
app.config.from_object('config') # Load configuration from config.py and particularly the DBMS URI
with app.app_context():
    db.init_app(app) # It connects the SQLAlchemy db object with the Flask app and the DBMS engine
    db.create_all() # Create the database tables for all the models

    

@app.route("/")
def index():
    return render_template("index.html", posts=BlogPost.query.all())

@app.route("/create", methods=["GET"])
def create_post_page():
    return render_template("create.html")
@app.route("/create", methods=["POST"])
def create_post_action():
    post = BlogPost(
        title=request.form["title"],
        content=request.form["content"],
        author=request.form["author"],
        )
    db.session.add(post)
    db.session.commit()
    return redirect(url_for("index"))
@app.route("/post/<int:post_id>")
def post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template("post.html", post=post)

@app.route("/stats")
def stats():
    post_lengths = BlogPost.get_post_lengths()
    return render_template("stats.html",
                           average_length=mean(post_lengths),
                           median_length=median(post_lengths),
                           max_length=max(post_lengths),
                           min_length=min(post_lengths),
                           total_length=sum(post_lengths),
                           )