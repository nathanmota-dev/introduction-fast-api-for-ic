from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class Mensagem(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(
        #TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
