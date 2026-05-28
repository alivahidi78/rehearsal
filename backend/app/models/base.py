from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import Integer, DateTime, func

class Base(DeclarativeBase):
    # TODO eventually replace with UUID
    id = mapped_column(Integer, primary_key=True)
    
class TimestampMixin:
    created_at = mapped_column(DateTime, server_default=func.now())
    updated_at = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    