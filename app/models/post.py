import uuid
from datetime import datetime
from app.models.user import User
from app.extensions import db


class Post(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    title = db.Column(db.String(150))
    content = db.Column(db.Text)
    is_published = db.Column(db.Boolean, default=False)
    views = db.Column(db.Integer, default=0)
    author_id = db.Column(db.String(36), db.ForeignKey('user.id'))
    parent_id = db.Column(db.String(36), db.ForeignKey('post.id'))
    category_id = db.Column(db.String(36), db.ForeignKey('category.id'))
    tags = db.relationship('Tag', secondary='post_tag',
                           backref=db.backref('posts', lazy='dynamic'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Category(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))
    posts = db.relationship('Post', backref='category', lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


post_tag = db.Table('post_tag',
                    db.Column('id', db.Integer, primary_key=True),
                    db.Column('post_id', db.String(36),
                              db.ForeignKey('post.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                    )


class Comment(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    text = db.Column(db.Text)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'))
    post_id = db.Column(db.String(36), db.ForeignKey('post.id'))
    parent_id = db.Column(db.String(36), db.ForeignKey('comment.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
