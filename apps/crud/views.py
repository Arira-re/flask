from functools import wraps
from flask import Blueprint, render_template, url_for, redirect, flash
from apps.crud.models import User
from apps.crud.forms import UserForm
from apps.app import db
from flask_login import login_required, current_user

crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
)

# 管理者のみアクセス可能にするデコレータ
# これ便利だね
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            flash('管理者のみアクセス可能です')
            return redirect(url_for('blogs.index'))
        return f(*args, **kwargs)
    return decorated_function

@crud.route("/")
@login_required
@admin_only
def index():
    users = User.query.all()
    return render_template("crud/index.html", users=users)

@crud.route("/users/new", methods=["GET", "POST"])
@login_required
@admin_only
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.index"))
    return render_template("crud/create.html", form=form)

@crud.route("/users")
@login_required
@admin_only
def users():
    users = User.query.all()
    return render_template("crud/index.html", users=users)

@crud.route("/users/<int:user_id>", methods=["GET", "POST"])
@login_required
@admin_only
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    return render_template("crud/edit.html", form=form, user=user)

@crud.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required
@admin_only
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("crud.users"))


