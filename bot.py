# -*- coding: utf-8 -*-
import telebot
from telebot import types, logger
from telebot.types import  InputMediaPhoto, InputMediaVideo, InputMediaDocument
import pandas as pd

import sys
import logging
import msg
import os
import keybords

import utils
from sqliteormmagic import SQLiteDB
import sqliteormmagic as som


from config import TOKEN, ADMIN_LIST

bot = telebot.TeleBot(token=TOKEN, parse_mode='HTML', skip_pending=True)    
bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("start", "Запуск бота"),
    ],)
db_users = SQLiteDB('users.db')


def main():
    @bot.message_handler(commands=['start'])
    def start_fnc(message):
        utils.cr_table_users(message)
        db_users.create_table('reklama', [
        ("from_user_id", 'INTEGER'), 
        ("from_user_username", 'TEXT'), 
        ("reg_time", 'TEXT'),       
        ("utm_code", 'TEXT'),                         
        ])
        unique_code = utils.extract_unique_code(message.text)
        print(unique_code)

        if unique_code:  # if the '/start' command contains a unique_code
            db_users.ins_unique_row('reklama', [
            ("from_user_id", message.from_user.id), 
            ("from_user_username", message.from_user.username), 
            ("reg_time", utils.get_msk_time()),         
            ("utm_code", unique_code),    
            ])  
            bot.send_message(chat_id=message.from_user.id, text=msg.start_msg_user,reply_markup=keybords.user_menu_main())

        else:
            # with open('1.jpeg', mode='rb') as f1:
            #     with open('2.jpeg', mode='rb') as f2:
            #         with open('3.jpeg', mode='rb') as f3:
            #             with open('video.mp4', mode='rb') as video:
                            
            #                 bot.send_media_group(chat_id=message.from_user.id, media=[
            #                     InputMediaPhoto(media=f1), 
            #                     InputMediaPhoto(media=f2), 
            #                     InputMediaVideo(media=video),
            #                     InputMediaPhoto(media=f3, caption='фото 3')
            #                     ])
           
            bot.send_message(chat_id=message.from_user.id, text=msg.start_msg_user,reply_markup=keybords.user_menu_main())             
    
    @bot.message_handler(commands=['admin'])
    def start_fnc(message):
        if message.from_user.id in ADMIN_LIST:
            bot.send_message(chat_id=message.from_user.id, text=msg.start_msg_admin, reply_markup=keybords.admin_menu_main())

    @bot.message_handler(content_types=['photo'])
    def get_photo(message):
        foto = message.photo[len(message.photo) - 1].file_id
        file_info = bot.get_file(foto)
        photo = bot.download_file(file_info.file_path)
        msg = bot.save_photo()

    # @bot.message_handler(content_types=['photo', 'video'])
    # def get_photo(message):
    #     type_data = ''
    #     if message.photo:
    #             type_data = message.photo[len(message.photo) - 1].file_id
    #     elif message.video:
    #             type_data = message.video.file_id
                
    #     if message.media_group_id:
    #         current_user = message.from_user.id
    #         media_group_id = user_data[current_user].get('media_group_id', 0)

    #         if media_group_id == message.media_group_id:
    #             # если не изменилось, значит это не первое фото в группе и ничего постить не надо
                
    #             file_info = bot.get_file(type_data)
    #             all_data = bot.download_file(file_info.file_path)
    #             with open(file=f"all_data/{media_group_id}__{type_data}", mode='wb') as f:
    #                 f.write(all_data)
    #             print('**************все фото загружены*************')
    #         else:
    #             # в остальном случае - значит начало нового блока картинок - обновляем id группы и отсылаем сообщение
    #             file_info = bot.get_file(type_data)
    #             all_data = bot.download_file(file_info.file_path)
    #             with open(file=f"all_data/{media_group_id}__{type_data}", mode='wb') as f:
    #                 f.write(all_data)
    #             user_data[current_user]['media_group_id'] = message.media_group_id
            
    #     else:
    #         # здесь надо расписать для одиночных документов или ваще выкинуть это в другой хендлер

    #         file_info = bot.get_file(type_data)
    #         all_data = bot.download_file(file_info.file_path)
    #         with open(file=f"photos/{type_data}", mode='wb') as f:
    #             f.write(all_data)


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
        # клиентская часть
        if call.data == 'about':
            db_users.upd_element_in_column(table_name='users', set_upd_par_name='about_time', set_key_par_name=utils.get_msk_time(), upd_column_name='from_user_id', key_column_name=call.from_user.id)
            bot.send_message(chat_id=call.from_user.id, text=msg.about_msg, reply_markup=keybords.back())

        elif call.data == 'faq':
            db_users.upd_element_in_column(table_name='users', set_upd_par_name='faq_time', set_key_par_name=utils.get_msk_time(), upd_column_name='from_user_id', key_column_name=call.from_user.id)
            bot.send_message(chat_id=call.from_user.id, text=msg.faq_msg, reply_markup=keybords.back())
                              

        elif call.data == 'contacts':
            db_users.upd_element_in_column(table_name='users', set_upd_par_name='contacts_time', set_key_par_name=utils.get_msk_time(), upd_column_name='from_user_id', key_column_name=call.from_user.id)
            bot.send_message(chat_id=call.from_user.id, text=msg.contacts_msg, reply_markup=keybords.back())  

        elif call.data == 'back':
            bot.send_message(chat_id=call.from_user.id, text=msg.start_msg_user,reply_markup=keybords.user_menu_main())

        # админская часть
        elif call.data == 'report_utm':
            if call.from_user.id in ADMIN_LIST:
                connection = som.create_connection('users.db')
                query = f"""
                SELECT * FROM reklama 
                """
                all_records = pd.read_sql_query(query, connection)
                len_of_records = len(all_records['from_user_id'])
                all_records.to_excel('report.xlsx', index=False)
                connection.close()
                with open('report.xlsx', mode='rb') as filename:
                    bot.send_document(call.from_user.id, document=filename, caption=f'Всего {len_of_records} переходов. Отчет по статистике переходов по ссылкам в прикрепленном файле')
        
        elif call.data == 'report_users':
            if call.from_user.id in ADMIN_LIST:
                connection = som.create_connection('users.db')
                query = f"""
                SELECT * FROM users 
                """
                all_records = pd.read_sql_query(query, connection)
                len_of_records = len(all_records['from_user_id'])
                all_records.to_excel('report.xlsx', index=False)
                connection.close()
                with open('report.xlsx', mode='rb') as filename:
                    bot.send_document(call.from_user.id, document=filename, caption=f'Всего {len_of_records} переходов. Отчет по статистике пользователей в прикрепленном файле')



    bot.infinity_polling()

if __name__ == "__main__":
    main()

    