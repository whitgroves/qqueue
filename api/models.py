import api
# from flask_login import UserMixin

class User(api.db.Model):
    id = api.db.Column(api.db.Integer, primary_key=True)
    email = api.db.Column(api.db.String(128), index=True, unique=True)
    password_hash = api.db.Column(api.db.String(128))

    def __repr__(self):
        return f'<User {self.id}: {self.email}>'

# # allows flask-login to use User as an auth object
# @api.login.user_loader
# def load_user(id):
#     return User.query.get(int(id))

class Vendor(api.db.Model):
    id = api.db.Column(api.db.Integer, primary_key=True)
    email = api.db.Column(api.db.String(128), index=True, unique=True)
    password_hash = api.db.Column(api.db.String(128))

    def __repr__(self):
        return f'<Vendor {self.id}: {self.email}>'

class Product(api.db.Model):
    id = api.db.Column(api.db.Integer, primary_key=True)
    name = api.db.Column(api.db.String(128))
    tagline = api.db.Column(api.db.String(256))
    image_url = api.db.Column(api.db.String(256))
    image_thumbnail = api.db.Column(api.db.String(256))
    website = api.db.Column(api.db.String(256))
    qty = api.db.Column(api.db.Integer)
    price = api.db.Column(api.db.Float)
    vendor_id = api.db.Column(api.db.Integer)
    detail = api.db.Column(api.db.String(512))

    def __repr__(self):
        return f'<Product {self.id}: {self.name}>'