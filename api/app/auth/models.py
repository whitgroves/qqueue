from app import db

_TEXT_SHORT = db.String(128)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(_TEXT_SHORT, index=True, unique=True)
    username = db.Column(_TEXT_SHORT, index=True, unique=True)
    password_hash = db.Column(_TEXT_SHORT)

    def __repr__(self):
        return f'<User {self.id}: {self.email}>'

