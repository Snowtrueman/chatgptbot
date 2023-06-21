import datetime
from models import Base
from telebot import types
from loader import bot, logger
from keyboards import get_keyboard
from utils import get_help_text, check_user_password, make_verified, send_question,  get_tokens
from crud import get_user, create_user, add_to_history, clear_history, find_in_history, view_history


def init_menu(message: types.Message) -> None:
    """
    Initializes main(basic) menu.
    Args:
        message: User message.
    """

    bot.send_message(message.chat.id, "Please choose the action", reply_markup=get_keyboard("base"))


@bot.message_handler(commands=["start", "help"])
def commands_handler(message: types.Message) -> None:
    """
    Handles commands /start and /help.
    Args:
        message: User message.
    """

    match message.text:
        case "/start":
            user = get_user(message.from_user.id)
            if user and not user.is_verified:
                ask_for_password(message)
            elif user and user.is_verified:
                bot.reply_to(message, "👋 Welcome back, {}!".format(message.from_user.first_name))
                init_menu(message)
            else:
                ask_for_password(message)
        case "/help":
            bot.reply_to(message, get_help_text())


def ask_for_password(message: types.Message) -> None:
    """
    Asks user for password and registers next step for it verification.
    Args:
        message: User message.
    """

    bot.reply_to(message, "Please enter your password to grant access.")
    bot.register_next_step_handler(message, check_user_password_handler)


def check_user_password_handler(message: types.Message) -> None:
    """
    Gives access to the bot or displays an error message.
    Args:
        message: User message.
    """

    user = get_user(message.from_user.id)
    if check_user_password(message.text.strip()):
        if user:
            make_verified(message.from_user.id)
            bot.reply_to(message, "👋 Welcome {}!".format(message.from_user.first_name))
        else:
            create_user(telegram_user_id=message.from_user.id, telegram_user_name=message.from_user.first_name,
                        chat_id=message.chat.id, is_verified=True)
        init_menu(message)
    else:
        bot.reply_to(message, "😕 Sorry, but the password is not correct. Please check it and restart bot.")


def is_verified(message: types.Message | types.CallbackQuery) -> bool | None:
    """
    Verifies the user's authority to act with the bot.
    Args:
        message: User message or Callback.

    Returns:
        True if user has passed the verification else inits the verification procedure.
    """

    if type(message) == types.CallbackQuery:
        user_id = message.from_user.id
        chat_id = message.message.chat.id
        message = message.message
    else:
        user_id = message.from_user.id
        chat_id = message.chat.id
        message = message
    user = get_user(user_id)
    if user.is_verified:
        return True
    else:
        bot.send_message(chat_id, "You have not yet been verified. Please enter your password to grant access.")
        ask_for_password(message)


@bot.callback_query_handler(func=lambda call: call.data == "ask")
def ask_question_handler(call: types.CallbackQuery) -> None:
    """
    Asks the user to enter a question.
    Args:
        call: Callback message.
    """

    if is_verified(call):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Please enter your question")
        bot.register_next_step_handler(call.message, user_question_handler)


def user_question_handler(message: types.Message) -> None:
    """
    Processes the user request, interacts with the OpenAI API and prints the response.
    Args:
        message: User message.
    """

    if is_verified(message):
        bot.send_message(message.chat.id, "Trying to answer... It may take a while")
        question_id = add_to_history(message.text, telegram_user_id=message.from_user.id)
        answer = send_question(message.text)
        if question_id:
            add_to_history(answer, question_id=question_id)
        bot.send_message(message.chat.id, answer)
        init_menu(message)


@bot.callback_query_handler(func=lambda call: call.data == "clear")
def delete_history_handler(call: types.CallbackQuery) -> None:
    """
    Clears the user's question and answer history.
    Args:
        call: Callback message.
    """

    if is_verified(call):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        clear_history(call.from_user.id)
        bot.send_message(call.message.chat.id, "Your request history was successfully deleted")
        init_menu(call.message)


@bot.callback_query_handler(func=lambda call: call.data == "search")
def search_in_history_handler(call: types.CallbackQuery) -> None:
    """
    Requests a keyword to search for.
    Args:
        call: Callback message.
    """

    if is_verified(call):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Please provide your search phrase")
        bot.register_next_step_handler(call.message, user_search_handler)


def user_search_handler(message: types.Message) -> None:
    """
    Searches through the user's question history.
    Args:
        message: User message.
    """

    if is_verified(message):
        search_results = find_in_history(message.from_user.id, message.text)
        msg_for_user = ""
        if search_results:
            for result in enumerate(search_results):
                msg_for_user += f"{result[0]+1}. " \
                                f"Дата: {datetime.datetime.strftime(result[1][1], '%Y.%m.%d, %H:%M:%S')}.\n" \
                                f"Вопрос: {result[1][0]}. \n"
        else:
            msg_for_user += "Nothing was found for your query."
        bot.send_message(message.chat.id, msg_for_user)
        init_menu(message)


@bot.callback_query_handler(func=lambda call: call.data == "history")
def view_history_handler(call: types.CallbackQuery) -> None:
    """
    Prints the entire history of the user's questions and answers.
    Args:
        call: Callback message.
    """

    if is_verified(call):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        history_result = view_history(call.from_user.id)
        msg_for_user = ""
        if history_result:
            for result in enumerate(history_result):
                msg_for_user += f"{result[0]+1}. " \
                                f"Дата: {datetime.datetime.strftime(result[1][1], '%Y.%m.%d, %H:%M:%S')}\n" \
                                f"Вопрос: {result[1][0]} \n" \
                                f"Дата: {datetime.datetime.strftime(result[1][3], '%Y.%m.%d, %H:%M:%S')}\n" \
                                f"Ответ: {result[1][2]} \n"
        else:
            msg_for_user += "Can't find anything in history."
        bot.send_message(call.message.chat.id, msg_for_user)
        init_menu(call.message)


@bot.callback_query_handler(func=lambda call: call.data == "tokens")
def tokens_left_handler(call: types.CallbackQuery) -> None:
    """
    Prints the account balance in tokens.
    Args:
        call: Callback message.
    """

    if is_verified(call):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        tokens_left = get_tokens()
        bot.send_message(call.message.chat.id, f"Tokens left: {tokens_left}")
        init_menu(call.message)


if __name__ == "__main__":
    Base.metadata.create_all()
    while True:
        try:
            bot.polling()
            logger.info("Bot successfully started")
        except Exception as e:
            pass
            logger.critical(f"Bot is down because and exception has been raised {e.__class__}\n{e}")
            logger.info("Trying to restart")
