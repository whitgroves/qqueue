from app import db
from app.utils.database import Column, ColType


class Product(db.Model):
    __tablename__ = 'products'

    id = Column.pk_id()
    name = db.Column(ColType.text_short)
    detail = db.Column(ColType.text_long)
    # tagline = db.Column(ColType.text_mid)
    # image_url = db.Column(ColType.text_mid)
    # image_thumbnail = db.Column(ColType.text_mid)
    # website = db.Column(ColType.text_mid)
    # qty = db.Column(ColType.number)
    # price = Column.fiat()
    # vendor_id = db.Column(ColType.number)

    def __repr__(self) -> str:
        return f'<Product {self.id}: {self.name}>'

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'detail': self.detail,
            # 'image_url': self.image_url,
            # 'price': self.price, 
        }
