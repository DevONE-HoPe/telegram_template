# ruff: noqa: TC001, TC003, A003, F821
from __future__ import annotations

from sqlalchemy import BigInteger, Text, String
from sqlalchemy.orm import Mapped, mapped_column

from tg_bot_template.database.models.base import Base, big_int_pk, created_at


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[big_int_pk]
    username: Mapped[str | None] = mapped_column(String(50))
    created_at: Mapped[created_at]
    taps: Mapped[int] = mapped_column(BigInteger, server_default="0", nullable=False)
    name: Mapped[str | None] = mapped_column(Text)
    info: Mapped[str | None] = mapped_column(Text)
    photo: Mapped[str | None] = mapped_column(Text)
