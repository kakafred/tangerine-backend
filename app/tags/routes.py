from flask import jsonify, request
from app.authentication.permissions import role_required
from app.extensions import db
from app.models.post import Tag
from app.tags import bp


@bp.route('/health-check')
def health_check():
    try:
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/', methods=['GET'])
def get_tags():
    tags = Tag.query.all()
    tags_list = [{
        "id": tag.id, "name": tag.name,
        "created_at": tag.created_at,
        "updated_at": tag.updated_at} for tag in tags]
    return jsonify(tags_list)


@bp.route('/', methods=['POST'])
@role_required('admin')
def create_tag():
    data = request.json
    name = data.get('name')

    if not name:
        return jsonify({"error": "Tag name is required"}), 400

    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()

    return jsonify({"message": "tag created successfully"}), 201


@bp.route('/<int:tag_id>', methods=['PUT'])
@role_required('admin')
def update_tag(tag_id):
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({"error": "Tag not found"}), 404

    data = request.json
    name = data.get('name')

    if not name:
        return jsonify({"error": "Tag name is required"}), 400

    tag.name = name
    db.session.commit()

    return jsonify({"message": "Tag updated successfully"})


@bp.route('/<int:tag_id>', methods=['DELETE'])
@role_required('admin')
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({"error": "Tag not found"}), 404

    db.session.delete(tag)
    db.session.commit()

    return jsonify({"message": "Tag deleted successfully"})
