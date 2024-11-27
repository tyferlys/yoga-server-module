from datetime import datetime

from sqlalchemy import String, Boolean, Integer, ForeignKey, Text, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.config import Base


class User(Base):
    __tablename__ = "t_users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(256), unique=True)
    password: Mapped[str] = mapped_column(String(256))
    is_admin: Mapped[bool] = mapped_column(Boolean)
    permission_study: Mapped[bool] = mapped_column(Boolean)


class YogaPose(Base):
    __tablename__ = "t_yoga_poses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    title_sanskrit: Mapped[str] = mapped_column(String(256))
    title_transliteration: Mapped[str] = mapped_column(String(256))
    title_russian: Mapped[str] = mapped_column(String(256))


class ResultPrediction(Base):
    __tablename__ = "t_result_predictions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_user: Mapped[int] = mapped_column(BigInteger(), ForeignKey("t_users.id"), nullable=True)
    image: Mapped[str] = mapped_column(Text())
    answer: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False))

    is_right: Mapped[bool] = mapped_column(Boolean(), nullable=True)
    right_answer_system: Mapped[int] = mapped_column(BigInteger(), ForeignKey("t_yoga_poses.id"), nullable=True)
    right_answer_sanskrit: Mapped[str] = mapped_column(String(256), nullable=True)
    right_transliteration: Mapped[str] = mapped_column(String(256), nullable=True)
    right_answer_russian: Mapped[str] = mapped_column(String(256), nullable=True)

    user = relationship("User")
    right_answer_system_entity = relationship("YogaPose", lazy="joined")