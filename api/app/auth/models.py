from app import db
from app.utils.database import Column, ColType


class User(db.Model):
    __tablename__ = 'users'

    id = Column.pk_id()
    email = Column.unique_index()
    # username = Column.unique_index()
    password_hash = db.Column(ColType.text_short)

    def __repr__(self) -> str:
        return f'<User {self.id}: {self.email}>'

    def to_dict(self) -> dict:
        return {'id': self.id, 'email': self.email}
