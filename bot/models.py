import datetime
from db import get_db
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean


Base = declarative_base(bind=get_db())


class Users(Base):
    """
    User model.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_user_id = Column(Integer, nullable=False, unique=True)
    telegram_user_name = Column(String, nullable=False)
    chat_id = Column(Integer, nullable=False, unique=True)
    is_verified = Column(Boolean, nullable=False, default=False)

    user_questions = relationship("Questions", backref="user", cascade="all,delete")


class Questions(Base):
    """
    User questions model.
    """

    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(Users.id, ondelete="CASCADE"), nullable=False)
    text = Column(String, nullable=False)
    asked = Column(DateTime, default=datetime.datetime.now, nullable=False)

    question_answer = relationship("Answers", backref="question", cascade="all,delete")


class Answers(Base):
    """
    Ai answers model.
    """

    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey(Questions.id, ondelete="CASCADE"), nullable=False)
    text = Column(String, nullable=False)
    answered = Column(DateTime, default=datetime.datetime.now, nullable=False)
