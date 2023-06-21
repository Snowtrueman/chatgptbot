from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard(keyboard_type: str) -> InlineKeyboardMarkup:
    """
    Generates different keyboards according to "keyboard_type".
    Args:
        keyboard_type: Required keyboard type.

    Returns:
        Inline keyboard markup.
    """

    match keyboard_type:
        case "base":
            markup = InlineKeyboardMarkup()
            markup.row_width = 1
            markup.add(InlineKeyboardButton("📢 Ask a question", callback_data="ask"))
            markup.add(InlineKeyboardButton("📆 View history", callback_data="history"))
            markup.add(InlineKeyboardButton("🔍 Find a question in history", callback_data="search"))
            markup.add(InlineKeyboardButton("🗑 Clear history", callback_data="clear"))
            markup.add(InlineKeyboardButton("💵 Tokens left", callback_data="tokens"))

    return markup


