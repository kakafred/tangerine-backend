from MySQLdb import IntegrityError
from flask import jsonify, request
from flask_login import current_user
from app.authentication.permissions import role_required
from app.extensions import db
from app.models.post import Category, Comment, Post, Tag
from app.models.user import User
from app.posts import bp


@bp.route('/health-check')
def health_check():
    try:
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/', methods=['GET'])
def get_posts():
    posts = Post.query.filter_by(is_published=True)
    posts_list = []
    for post in posts:
        category_name = Category.query.get(
            post.category_id).name if post.category_id else None
        parent_name = Post.query.get(
            post.parent_id).title if post.parent_id else None

        author = User.query.get(post.author_id)
        author_username = author.username if author else None
        author_avatar = author.avatar_url if author else None

        comment_count = Comment.query.filter_by(post_id=post.id).count()

        post_data = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "views": post.views,
            "comments": comment_count,
            "parent_name": parent_name,
            "category_name": category_name,
            "author": author_username,
            "author_avatar": author_avatar,
            "tags": [tag.name for tag in post.tags],
            "created_at": post.created_at,
            "updated_at": post.updated_at
        }
        posts_list.append(post_data)
    return jsonify(posts_list)


@bp.route('/', methods=['POST'])
@role_required('admin')
def create_post():
    data = request.json
    title = data.get('title')
    content = data.get('content')
    is_published = data.get('is_published', False)
    views = data.get('views', 0)
    author_id = current_user.id
    parent_id = data.get('parent_id')
    category_id = data.get('category_id')
    tags = data.get('tags', [])

    post = Post(
        title=title,
        content=content,
        is_published=is_published,
        views=views,
        author_id=author_id,
        category_id=category_id
    )

    if parent_id:
        post.parent_id = parent_id

    for tag_name in tags:
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.session.add(tag)
        post.tags.append(tag)

    db.session.add(post)
    db.session.commit()

    return jsonify({"message": "Post created successfully", "post_id": post.id}), 201


@bp.route('/<string:post_id>', methods=['PUT'])
@role_required('admin')
def update_post(post_id):
    post = Post.query.get(post_id)

    if not post:
        return jsonify({"error": "Post not found"}), 404

    data = request.json
    title = data.get('title')
    content = data.get('content')
    is_published = data.get('is_published')
    views = data.get('views')
    category_id = data.get('category_id')
    parent_id = data.get('parent_id')
    tags = data.get('tags', [])

    if title:
        post.title = title
    if content:
        post.content = content
    if is_published is not None:
        post.is_published = is_published
    if views is not None:
        post.views = views
    if category_id:
        post.category_id = category_id
    if parent_id:
        post.parent_id = parent_id

    post.tags.clear()
    for tag_name in tags:
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.session.add(tag)
        post.tags.append(tag)

    db.session.commit()

    return jsonify({"message": "Post updated successfully"})


def delete_post_and_children(post):
    children = Post.query.filter_by(parent_id=post.id).all()
    for child in children:
        delete_post_and_children(child)

    db.session.delete(post)
    db.session.commit()


@bp.route('/<string:post_id>', methods=['DELETE'])
@role_required('admin')
def delete_post(post_id):
    post = Post.query.get(post_id)

    if not post:
        return jsonify({"error": "Post not found"}), 404

    try:
        db.session.delete(post)
        db.session.commit()
    except IntegrityError:
        return jsonify({"message": "This post has related child posts. Please delete them first."}), 409

    return jsonify({"message": "Post deleted successfully"})
