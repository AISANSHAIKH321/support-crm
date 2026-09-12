from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, unique=True, index=True)
    customer_name = Column(String)
    customer_email = Column(String)
    subject = Column(String)
    description = Column(Text)
    status = Column(String, default="Open")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, index=True)
    note_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)