from app import db
from app.utils.database import ColType


class User(db.Model):
    __tablename__ = 'users'

    id = ColType.pk_id()
    email = ColType.unique_index()
    password_hash = db.Column(ColType.text_short)
    
    products = db.relationship('Product',
                               backref='user',
                               cascade='all, delete-orphan',
                               lazy='dynamic')

    def __repr__(self) -> str:
        return f'<User {self.id}: {self.email}>'

    def to_dict(self) -> dict:
        return {'id': self.id, 'email': self.email}
