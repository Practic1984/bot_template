# -*- coding: utf-8 -*-
import telebot
from telebot import types, logger
import sys
import logging
import msg
import os
import keybords
from config import TOKEN
from sqliteormmagic import SQLiteDB




# sys.stdout = open("stdout.txt", "a", encoding="utf-8")
# # sys.stderr = open("stderr.txt", "a", encoding="utf-8")

# # логирование
# db_users = SQLiteDB('users.db')
# logger = telebot.logger
# logging.basicConfig(level=logging.DEBUG, filename="system.log",filemode="a",
#                     format="%(asctime)s %(levelname)s %(message)s", encoding='utf-8')
# handler = logging.FileHandler('log_res.txt', mode='a', encoding='utf-8')
# logger.addHandler(handler)
# telebot.logger.setLevel(level=logging.DEBUG)


answer_options = ["Финансы", "Здоровье", "Успех", "Духовность"]
answer_options_dic = {
    0 : "Финансы",
    1 : "Здоровье",
    2 : "Успех",
    3 : "Духовность"
}


bot = telebot.TeleBot(token=TOKEN, parse_mode='HTML', skip_pending=True)    
bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("start", "Запуск бота"),
    ],)


def main():
    @bot.message_handler(commands=['start'])
    def start_fnc(message):
        bot.send_message(chat_id=message.from_user.id, text=msg.start_msg,reply_markup=keybords.menu_next())
    
    # @bot.message_handler(content_types=['photo'])
    # def get_photo(message):
    #     foto = message.photo[len(message.photo) - 1].file_id
    #     file_info = bot.get_file(foto)
    #     photo = bot.download_file(file_info.file_path)
    #     msg = bot.save_photo()

    @bot.message_handler(content_types=['photo', 'video'])
    def get_photo(message):
        type_data = ''
        if message.photo:
                type_data = message.photo[len(message.photo) - 1].file_id
        elif message.video:
                type_data = message.video.file_id
                
        if message.media_group_id:
            current_user = message.from_user.id
            media_group_id = user_data[current_user].get('media_group_id', 0)

            if media_group_id == message.media_group_id:
                # если не изменилось, значит это не первое фото в группе и ничего постить не надо
                
                file_info = bot.get_file(type_data)
                all_data = bot.download_file(file_info.file_path)
                with open(file=f"all_data/{media_group_id}__{type_data}", mode='wb') as f:
                    f.write(all_data)
                print('**************все фото загружены*************')
            else:
                # в остальном случае - значит начало нового блока картинок - обновляем id группы и отсылаем сообщение
                file_info = bot.get_file(type_data)
                all_data = bot.download_file(file_info.file_path)
                with open(file=f"all_data/{media_group_id}__{type_data}", mode='wb') as f:
                    f.write(all_data)
                user_data[current_user]['media_group_id'] = message.media_group_id
            
        else:
            # здесь надо расписать для одиночных документов или ваще выкинуть это в другой хендлер

            file_info = bot.get_file(type_data)
            all_data = bot.download_file(file_info.file_path)
            with open(file=f"photos/{type_data}", mode='wb') as f:
                f.write(all_data)


    @bot.message_handler(content_types=['video'])
    def get_video(message):
        video = message.video.file_id
        file_info = bot.get_file(video)
        video = bot.download_file(file_info.file_path)

    
    @bot.message_handler(content_types=['document'])
    def get_document(message):
        document = message.document.file_id
        file_info = bot.get_file(document)
        document = bot.download_file(file_info.file_path)
        
    @bot.message_handler(commands=["poll"])
    def create_poll(message):
        bot.send_message(message.chat.id, "Выбрать категорию")


        bot.send_poll(
            chat_id=message.chat.id,
            allows_multiple_answers = True,
            question="Выбрать цель",
            options=answer_options,
            type="regular",
            is_anonymous=False,
            open_period = 60,
        )

    @bot.poll_answer_handler()
    def handle_poll(poll):
        print(poll)
        text = "Вы выбрали\n "
        for option_id in poll.option_ids:
            text += f"- {answer_options_dic[option_id]}\n"
        bot.send_message(chat_id=poll.user.id, text=text, reply_markup=keybords.menu_next())

        bot.stop_poll(chat_id=poll.user.id, message_id=poll.id)


    @bot.message_handler(content_types=['text'])
    def get_text(message):
        print(f"message {message.text}")


    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        pass
    
    bot.infinity_polling()

if __name__ == "__main__":
    main()

    