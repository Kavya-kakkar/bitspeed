from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, index=True)
    phoneNumber = Column("phone_number" ,String, nullable=True)
    email = Column(String, nullable=True)
    linkedId = Column("linked_id",Integer, nullable=True)
    linkPrecedence = Column("link_precedence",String)
    createdAt = Column("created_at",DateTime(timezone=True), server_default=func.now())
    updatedAt = Column("updated_at",DateTime(timezone=True), onupdate=func.now())
    deletedAt = Column("deleted_at",DateTime(timezone=True), nullable=True)


Base.metadata.create_all(bind=engine)