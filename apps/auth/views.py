from flask import Blueprint, render_template, redirect, url_for, flash, request
from apps.auth.forms import LoginForm, SignUpForm
from apps.crud.models import User
from apps.app import db
from flask_login import login_user, logout_user, current_user, login_required

# Blueprintのインスタンスを作成
auth = Blueprint(
    'auth',
    __name__,
    template_folder='templates',
)


@auth.route('/')
def index():
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        # 既存ユーザー確認
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        if user.is_duplicate_email():
            flash('このメールアドレスは既に登録されています')
            return render_template('auth/signup.html', form=form)

        db.session.add(user)
        db.session.commit()

        # ユーザー情報をセッションに格納する
        login_user(user)
        return redirect(url_for('crud.index'))
    return render_template('auth/signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            flash('ログインしました', 'success')
            login_user(user)
            if user.id == 1:
                return redirect(url_for('crud.index'))
            else:
                return redirect(url_for('blogs.index'))  # blogs.index へリダイレクト
        else:
            flash('メールアドレスまたはパスワードが間違っています')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('ログアウトしました', 'success')
    return redirect(url_for('auth.login'))