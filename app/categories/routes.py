from flask import jsonify, request
from app.authentication.permissions import role_required
from app.categories import bp
from app.extensions import db
from app.models.post import Category


@bp.route('/health-check')
def health_check():
    try:
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    categories_list = [{
        "id": category.id, "name": category.name,
        "description": category.description,
        "created_at": category.created_at,
        "updated_at": category.updated_at} for category in categories]
    return jsonify(categories_list)


@bp.route('/', methods=['POST'])
@role_required('admin')
def create_category():
    data = request.json
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({"error": "Category name is required"}), 400

    if not description:
        return jsonify({"error": "Category description is required"}), 400

    category = Category(name=name, description=description)
    db.session.add(category)
    db.session.commit()

    return jsonify({"message": "Category created successfully"}), 201


@bp.route('/<string:category_id>', methods=['PUT'])
@role_required('admin')
def update_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    data = request.json
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({"error": "Name is required"}), 400

    if not description:
        return jsonify({"error": "Category description is required"}), 400

    category.name = name
    category.description = description
    db.session.commit()

    return jsonify({"message": "Category updated successfully"})


@bp.route('/<string:category_id>', methods=['DELETE'])
@role_required('admin')
def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    db.session.delete(category)
    db.session.commit()

    return jsonify({"message": "Category deleted successfully"})
