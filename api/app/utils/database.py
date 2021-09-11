from app import db


class ColType(object):
    """
    Class to store constants for commonly used SQLAlchemy column types.
    Do not instantiate.
    """
    text_short = db.String(128)
    text_mid = db.String(256)
    text_long = db.String(512)
    number = db.Integer
    # for safekeeping:
    # https://docs.sqlalchemy.org/en/14/core/type_basics.html?highlight=integer#generic-types


class Column(object):
    """
    Class to generate specifically-configured, commonly-used SQLAlchemy columns.
    Do not instantiate.
    """
    
    @classmethod
    def pk_id(cls) -> db.Column:
        """
        Creates a primary key column for auto-incrementing numbers.

        Returns:
            db.Column: The id column.
        """
        return db.Column(ColType.number,
                         primary_key=True)  # auto-increments by default

    @classmethod
    def unique_index(cls, col_type: ColType = ColType.text_short) -> db.Column:
        """
        Creates an indexed column with a UNIQUE constraint.

        Args:
            col_type (ColType, optional): The type of the column. 
                                          Defaults to ColType.text_short.

        Returns:
            db.Column: The generated column.
        """
        return db.Column(col_type, unique=True, index=True)

    @classmethod
    def fiat(cls) -> db.Column:
        """
        Creates a column formatted to store fiat currency.

        Returns:
            db.Column: The generated column.
        """
        return db.Column(
            db.Numeric(precision=10, scale=2, decimal_return_scale=2))
