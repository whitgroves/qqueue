# import app
# # from flask_login import UserMixin

# class User(app.db.Model):
#     id = app.db.Column(app.db.Integer, primary_key=True)
#     email = app.db.Column(app.db.String(128), index=True, unique=True)
#     password_hash = app.db.Column(app.db.String(128))

#     def __repr__(self):
#         return f'<User {self.id}: {self.email}>'

# # # allows flask-login to use User as an auth object
# # @app.login.user_loader
# # def load_user(id):
# #     return User.query.get(int(id))

# class Vendor(app.db.Model):
#     id = app.db.Column(app.db.Integer, primary_key=True)
#     email = app.db.Column(app.db.String(128), index=True, unique=True)
#     password_hash = app.db.Column(app.db.String(128))

#     def __repr__(self):
#         return f'<Vendor {self.id}: {self.email}>'

# class Product(app.db.Model):
#     id = app.db.Column(app.db.Integer, primary_key=True)
#     name = app.db.Column(app.db.String(128))
#     tagline = app.db.Column(app.db.String(256))
#     image_url = app.db.Column(app.db.String(256))
#     image_thumbnail = app.db.Column(app.db.String(256))
#     website = app.db.Column(app.db.String(256))
#     qty = app.db.Column(app.db.Integer)
#     price = app.db.Column(app.db.Float)
#     vendor_id = app.db.Column(app.db.Integer)
#     detail = app.db.Column(app.db.String(512))

#     def __repr__(self):
#         return f'<Product {self.id}: {self.name}>'