import uuid
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(64), nullable=False, index=True)
    email = db.Column(db.String(120), nullable=False, index=True, unique=True)
    avatar_url = db.Column(db.String(255), nullable=False,
                           default="https://api.dicebear.com/7.x/identicon/svg?seed=tangerine&radius=10")
    password = db.Column(db.String(255), nullable=False)

    ROLES = ['reader', 'admin']
    role = db.Column(db.Enum(*ROLES), nullable=False, default='reader')

    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(id):
    return User.query.get(str(id))
