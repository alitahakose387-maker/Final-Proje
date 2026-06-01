from datetime import datetime
from typing import Optional

from flask_login import UserMixin
from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager


# --------------------------------------------------------------------------- #
#  Flask-Login user loader
# --------------------------------------------------------------------------- #
@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))


# --------------------------------------------------------------------------- #
#  User
# --------------------------------------------------------------------------- #
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    is_confirmed: Mapped[bool] = mapped_column(default=False)


    # İlişkiler
    prompts: Mapped[list["Prompt"]] = relationship(
        back_populates="author", lazy="dynamic"
    )
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="author", lazy="dynamic"
    )

    # Şifre yönetimi
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.username}>"


# --------------------------------------------------------------------------- #
#  Prompt
# --------------------------------------------------------------------------- #
class Prompt(db.Model):
    __tablename__ = "prompts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    prompt_text: Mapped[str] = mapped_column(Text)
    ai_tool: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # İlişkiler
    author: Mapped["User"] = relationship(back_populates="prompts")
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="prompt", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Prompt {self.title[:30]}>"


# --------------------------------------------------------------------------- #
#  Comment
# --------------------------------------------------------------------------- #
class Comment(db.Model):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    prompt_id: Mapped[int] = mapped_column(ForeignKey("prompts.id"))

    # İlişkiler
    author: Mapped["User"] = relationship(back_populates="comments")
    prompt: Mapped["Prompt"] = relationship(back_populates="comments")

    def __repr__(self) -> str:
        return f"<Comment {self.id}>"
