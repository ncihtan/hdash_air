"""WebCache ORM Class."""
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.mysql import LONGTEXT
from hdash.db.db_base import Base
from typing import Union


class WebCache(Base):
    """MetaCache ORM Class."""

    __tablename__ = "web_cache"
    web_cache_id = Column(Integer, primary_key=True, autoincrement=True)
    file_name: Union[str, Column] = Column(String(255))
    content: Union[str, Column] = Column(LONGTEXT)

    def __repr__(self):
        """Get summary."""
        return f"<WebCache({self.web_cache_id}, {self.file_name})>"
