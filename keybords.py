from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
def menu_next():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Погнали дальше?", callback_data="next"),
    )

    return markup
