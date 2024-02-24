from datetime import datetime
from flask import jsonify, request
from flask_login import current_user, login_required
from app.authentication.permissions import role_required
from app.comments import bp
from app.extensions import db
from app.models.post import Comment, Post


@bp.route('/health-check')
def health_check():
    try:
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/<string:post_id>', methods=['GET'])
def get_post_comments(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    comments = [{"id": comment.id,
                 "content": comment.text,
                 "created_at": comment.created_at
                 }
                for comment in post.comments]
    return jsonify(comments)


@bp.route('/', methods=['POST'])
@login_required
def create_comment():
    data = request.json
    text = data.get('text')
    user_id = current_user.id
    post_id = data.get('post_id')
    parent_id = data.get('parent_id')

    if not text:
        return jsonify({"error": "Text is required"}), 400

    comment = Comment(
        text=text,
        user_id=user_id,
        post_id=post_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    if parent_id:
        comment.parent_id = parent_id

    db.session.add(comment)
    db.session.commit()

    return jsonify({"message": "Comment created successfully", "comment_id": comment.id}), 201


@bp.route('/<string:comment_id>', methods=['PUT'])
@login_required
def update_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    if current_user.id != comment.user_id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    text = data.get('text')

    if not text:
        return jsonify({"error": "Text is required"}), 400

    comment.text = text
    comment.updated_at = datetime.utcnow()

    db.session.commit()

    return jsonify({"message": "Comment updated successfully"})


@bp.route('/<string:comment_id>', methods=['DELETE'])
@role_required('admin')
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    db.session.delete(comment)
    db.session.commit()

    return jsonify({"message": "Comment deleted successfully"})
