from models import Users, Questions, Answers
from sqlalchemy import exc
from loader import logger, session


def create_user(telegram_user_id: int, telegram_user_name: str, chat_id: int, is_verified=False) -> bool:
    """
    Performs operations on database to create new user.
    Args:
        telegram_user_id: User ID in Telegram.
        telegram_user_name: Username in Telegram.
        chat_id: Chat ID in Telegram.
        is_verified: Arg describing whether the user has been verified

    Returns:
        True if success else False.
    """

    try:
        user = Users(
            telegram_user_id=telegram_user_id,
            telegram_user_name=telegram_user_name,
            chat_id=chat_id,
            is_verified=is_verified
        )
        session.add(user)
        session.commit()
        logger.info(f"Successfully registered new user with telegram ID {telegram_user_id}")
        return True
    except exc.SQLAlchemyError:
        logger.error(f"Database error while registering new user with telegram ID {telegram_user_id}")
        return False


def get_user(telegram_user_id: int) -> Users | None:
    """
    Returns user object by specified user ID.
    Args:
        telegram_user_id: User ID in telegram.

    Returns:
        User object if found else None.
    """

    user = session.query(Users).filter(Users.telegram_user_id == telegram_user_id).one_or_none()
    if user:
        return user
    else:
        return None


def add_to_history(message_text: str, telegram_user_id: int = None, question_id: int = None) -> int | bool:
    """
    Writes questions and answers in database depending on question_id arg.
    If question_id is None then the incoming data is 100% a question.
    Args:
        message_text: The text of an answer or a question.
        telegram_user_id: User ID in telegram.
        question_id: The ID of a question (if we are saving the answer).

    Returns:
        Question ID if we heave saved a question for the future use when saving an answer, True if we successfully
        saved an answer, otherwise False.
    """

    try:
        if question_id is None:
            user = get_user(telegram_user_id)
            question = Questions(
                user_id=user.id,
                text=message_text
            )
            session.add(question)
            session.commit()
            return question.id
        else:
            answer = Answers(
                question_id=question_id,
                text=message_text
            )
            session.add(answer)
            session.commit()
            return True
    except exc.SQLAlchemyError:
        logger.error(f"Database error while adding {'question' if question_id is None else 'answer'} "
                     f"for user {telegram_user_id}")
        return False


def clear_history(telegram_user_id: int) -> bool:
    """
    Clears all questions and answers in DB for current user.
    Args:
        telegram_user_id: User ID in telegram.

    Returns:
        True if success else False.
    """

    try:
        user = get_user(telegram_user_id)
        questions = session.query(Questions).filter(Questions.user_id == user.id).all()
        for question in questions:
            session.delete(question)
        session.commit()
        return True
    except exc.SQLAlchemyError:
        logger.error(f"Database error while trying to clear history for user {telegram_user_id}")
        return False


def find_in_history(telegram_user_id: int, substring: str) -> list | bool:
    """
    Performs the request to OpenAi API.
    Args:
        telegram_user_id: User ID in telegram.
        substring: Substring to search for in history.

    Returns:
        The list with tuples (question text, date when it was asked).
    """

    try:
        user = get_user(telegram_user_id)
        result = session.query(Questions.text, Questions.asked).filter(Questions.user_id == user.id) \
            .filter(Questions.text.ilike(f"%{substring}%")).all()
        if result:
            return result
        else:
            return False
    except exc.SQLAlchemyError:
        logger.error(f"Database error while processing history search for user {telegram_user_id}"
                     f"with substring '{substring}'")
        return False


def view_history(telegram_user_id: int) -> list | bool:
    """
    Returns questions and answers history for user.
    Args:
        telegram_user_id: User ID in telegram.

    Returns:
        The list with tuples (question text, date when it was asked, answer, date when it was answered).
    """

    try:
        user = get_user(telegram_user_id)
        result = session.query(Questions.text, Questions.asked, Answers.text, Answers.answered).join(Answers) \
            .filter(Questions.user_id == user.id).filter(Questions.id == Answers.question_id).all()
        if result:
            return result
        else:
            return False
    except exc.SQLAlchemyError:
        logger.error(f"Database error while tying to view history for user {telegram_user_id}")
        return False
