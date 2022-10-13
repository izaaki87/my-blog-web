from Puppyblog.blog_posts.forms import PostForm
from Puppyblog import db
from flask import Blueprint, request, render_template, redirect, url_for, abort
from flask_login import login_required, current_user
from Puppyblog.models import BlogPost

blog = Blueprint("blog_posts", __name__)


@blog.route('/creat', methods=['GET', 'POST'])
@login_required
def create_blog():
  form = PostForm()
  if form.validate_on_submit():
    post = BlogPost(title=form.title.data, text=form.text.data, user_id=current_user.id)
    
    db.session.add(post)
    db.session.commit()
    return redirect(url_for("core.index"))
  
  return render_template("create_blog_post.html", form=form)


@blog.route("/<int:blog_post_id>/")
@login_required
def read_post(blog_post_id):
  post = BlogPost.query.get(blog_post_id)
  return render_template('blog_posts.html',  post=post)
  



@blog.route('/<int:blog_post_id>/update', methods=["GET", "POST"])
@login_required
def update(blog_post_id):
  post = BlogPost.query.get(blog_post_id)
  if post.author != current_user:
    abort(403)

  form = PostForm()

  if form.validate_on_submit(): 
    post.title = form.title.data
    post.text = form.text.data
    
    db.session.commit()
    return redirect(url_for('blog_posts.read_post', blog_post_id = post.id))
      
      
  elif request.method == "GET":
    form.title.data = post.title
    form.text.data = post.text
  
  return render_template("create_blog_post.html", form=form)
    

@blog.route('/<int:blog_post_id>/delete', methods=["GET", "POST"])
@login_required
def delete(blog_post_id):
  post = BlogPost.query.get_or_404(blog_post_id)
  
  if post.author != current_user:
    abort(403)
  
  db.session.delete(post)
  db.session.commit()
  return redirect(url_for("core.index"))
  
  
  





