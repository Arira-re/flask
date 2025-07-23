from apps.app import db
from datetime import datetime

class BlogPosts(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='blog_posts')
    title = db.Column(db.String(255), nullable=False)
    content_md = db.Column(db.Text, nullable=False)      # Markdown本文
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)