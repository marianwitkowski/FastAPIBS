
# Model fizyczny danych w bazie SQLite
from database import Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean, Integer, BigInteger
from sqlalchemy.sql import func

class Note(Base):
    __tablename__ = 'notes'
    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    category = Column(String, nullable=True)
    published = Column(Boolean, nullable=False, default=True)
    createdAt = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=func.now())
    updatedAt = Column(TIMESTAMP(timezone=True),
                       default=None, onupdate=func.now())
