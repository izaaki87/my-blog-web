
from Puppyblog import db
from flask import Blueprint, render_template,redirect,url_for, flash, abort, request

from flask_login import login_user,login_required, logout_user, current_user
from Puppyblog.models import  User, BlogPost
from Puppyblog.users.forms import LoginForm, RegisterForm, UpdateUserForm
from Puppyblog.users.pictures_handler import add_picture


users = Blueprint("users", __name__)


@users.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for("core.index"))


@users.route("/login", methods=["GET", "POST"])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user is not None and user.check_password(form.password.data):
      login_user(user)
      flash("you are login")
      
      next = request.args.get('next')
      if next == None and not next == ("/"):
        next = url_for("core.index")
      
      return redirect(next)

  return render_template("login.html", form=form)


@users.route("/register", methods=["GET", "POST"])
def register():
  form = RegisterForm()
  if form.validate_on_submit():
    users = User(email=form.email.data, username=form.username.data, 
                 password=form.password.data)
    db.session.add(users)
    db.session.commit()
    return redirect(url_for("users.login"))
  
  return render_template("register.html", form = form)


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
  form = UpdateUserForm()
  if form.validate_on_submit():
    if form.picture.data:
      username = current_user.username
      pic = add_picture(form.picture.data, username)
      current_user.profile_image = pic
    
    current_user.email = form.email.data
    current_user.username = form.username.data
    db.session.commit()
    return redirect(url_for('users.account'))
  
  elif request.method == "GET":
    form.email.data = current_user.email
    form.username.data = current_user.username
    
  
  profile_image = url_for("static", filename="profile_pic" + current_user.profile_image)
  return render_template("account.html", form=form, profile_image=profile_image)
    
    

@users.route("/<username>")
def users_post(username):
  page = request.args.get('page', 1, type=int)
  user = User.query.filter_by(username=username).first_or_404()
  blogpost = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
  return render_template('users_blog_post.html', user=user, blogpost=blogpost)
  
  

  
  
    



    
    