from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def user_menu_main():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("О проекте", callback_data="about"),
        InlineKeyboardButton("Faq", callback_data="faq"),
        InlineKeyboardButton("Отзывы", url='https://t.me/+1ndktCjS-Ik0NWEy'),                       
        InlineKeyboardButton("Контакты", callback_data="contacts"),         
        InlineKeyboardButton("Помощь", url='https://t.me/tatamartyanova'),                         
    )

    return markup


def admin_menu_main():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Отчет по клиентам", callback_data="report_users"),
        InlineKeyboardButton("Отчет по рекламе", callback_data="report_utm"),
        InlineKeyboardButton("Рассылка", callback_data="push_msg"),                       
                     
    )

    return markup