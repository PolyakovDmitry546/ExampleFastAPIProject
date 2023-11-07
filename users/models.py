from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    create_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
