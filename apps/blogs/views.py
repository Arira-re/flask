from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from apps.blogs.models import BlogPosts, Score
from apps.blogs.forms import BlogForm
from apps.app import db
from markdown import markdown
from apps.blogs.ai_utils import get_sentiment_score
from apps.crud.models import User

blogs = Blueprint(
    'blogs',
    __name__,
    template_folder='templates',
)


@blogs.route('/')
@login_required
def index():
    posts = BlogPosts.query.order_by(BlogPosts.created_at.desc()).all()
    user = User.query.get(current_user.id)
    return render_template('blogs/index.html', posts=posts,user=user)

@blogs.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = BlogForm()
    if form.validate_on_submit():
        try:
            post = BlogPosts(
                user_id=current_user.id,
                title=form.title.data,
                content_md=form.content_md.data
            )
            db.session.add(post)

            # 感情分析スコアの計算
            score_value = get_sentiment_score(form.content_md.data)
            print("感情スコア:", score_value)
            # Scoreテーブルに保存
            score = Score(user_id=current_user.id, score=score_value)
            db.session.add(score)

            # Userのave_scoreをスコアの平均値に更新
            user = User.query.get(current_user.id)
            all_scores = [s.score for s in user.scores]
            if all_scores:
                user.avg_score = sum(all_scores) / len(all_scores)
            else:
                user.avg_score = 0.0

            db.session.commit()
            flash('記事を投稿しました')
            return redirect(url_for('blogs.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'投稿保存時にエラー: {e}', 'error')
    return render_template('blogs/create.html', form=form)


@blogs.route('/<int:post_id>')
def detail(post_id):
    post = BlogPosts.query.get_or_404(post_id)
    html_body = markdown(post.content_md, extensions=[
                         'fenced_code', 'codehilite'])
    return render_template('blogs/detail.html', post=post, html_body=html_body)
