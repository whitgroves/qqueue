from decimal import Decimal
from typing import Any, Optional
from sqlalchemy import Column, String, Integer
from sqlalchemy.types import TypeDecorator


class Currency(TypeDecorator):
    """
            Converts Decimals from Python to Integers in Sqlite.
            Used to guarantee precision when storing monetary values in the db.
            """
    impl = Integer

    def __init__(self, scale: int = 2):
        TypeDecorator.__init__(self)
        self.scale = scale
        self.scale_multiplier = 10**self.scale  # used to scale from dec to int

    def process_bind_param(self, value: Optional[Any],
                           dialect: Any) -> Optional[Any]:
        if value is not None:
            value = int(Decimal(value) * self.scale_multiplier)
        return value

    def process_result_value(self, value: Optional[Any],
                             dialect: Any) -> Optional[Any]:
        if value is not None:
            value = Decimal(value) / self.scale_multiplier
        return value


class ColType(object):
    """
    Class to fetch commonly used SQLAlchemy column configurations. Do not instantiate.
    
    Reference:
        https://docs.sqlalchemy.org/en/14/core/type_basics.html?highlight=integer#generic-types
    """

    text_short = String(128)
    text_mid = String(256)
    text_long = String(512)
    fiat = Currency()

    @classmethod
    def pk_id(cls) -> Column:
        """
        Creates a PRIMARY KEY column that auto-increments by default.

        Returns:
            Column: An INT column configured as a primary key.
        """
        return Column(Integer, primary_key=True)

    @classmethod
    def unique_index(cls) -> Column:
        """
        Creates an indexed TEXT column with a UNIQUE constraint.
        
        Returns:
            Column: A TEXT column configured as a unique index.
        """
        return Column(ColType.text_short, unique=True, index=True)
