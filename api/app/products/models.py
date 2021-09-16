from app import db
from app.utils.database import ColType


class Product(db.Model):
    __tablename__ = 'products'

    id = ColType.pk_id()
    name = db.Column(ColType.text_short)
    detail = db.Column(ColType.text_long)
    tagline = db.Column(ColType.text_mid)
    image_url = db.Column(ColType.text_mid)
    price = db.Column(ColType.fiat)
    is_active = db.Column(db.Boolean)

    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self) -> str:
        return f'<Product {self.id}: {self.name}>'

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'detail': self.detail,
            'tagline': self.tagline,
            'image_url': self.image_url,
            'price': self.price,
            'seller_id': self.seller_id,
        }
