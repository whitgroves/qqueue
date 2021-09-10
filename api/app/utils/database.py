from app import db

class ColType(object):
    text_short = db.String(128)
    text_mid = db.String(256)
    text_long = db.String(512)
    number = db.Integer
    # for safekeeping:
    # https://docs.sqlalchemy.org/en/14/core/type_basics.html?highlight=integer#generic-types


class Column(object):

    @classmethod
    def primary_key(cls) -> db.Column:
        return db.Column(ColType.number, primary_key=True)  # auto-increments by default

    @classmethod
    def unique_index(cls) -> db.Column:
        return db.Column(ColType.text_short, index=True, unique=True)

    @classmethod
    def fiat(cls) -> db.Column:
        return db.Column(db.Numeric(precision=10, scale=2, decimal_return_scale=2))

