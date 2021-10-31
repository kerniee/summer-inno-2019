@bot.message_handler(func=lambda message: True)
def send_info(message):
    print(message.text)
    if message.forward_from:
        username = message.forward_from.username
        user_id = message.forward_from.id
        name = message.forward_from.first_name
    else:
        username = message.chat.username
        user_id = message.chat.id
        name = message.chat.first_name
    bot.send_message(chat_id=message.chat.id,
                     text='@{}\nId: {}\nFirst: {}'.format(
                         username, user_id, name
                     ))


@bot.message_handler(content_types=
                     ['document', 'photo'])
def to_cloud(message):
    m_type = message.content_type
    if m_type == 'document':
        info = bot.get_file(message.document.file_id)
    else:
        info = bot.get_file(message.photo[1].file_id)
    file_bytes = bot.download_file(info.file_path)
    with open(f'files/{info.file_path}', 'wb') as file:
        file.write(file_bytes)


@bot.inline_handler(func=lambda query:
                    'инфа' in query.query or
                    'info' in query.query or
                    'информация' in query.query)
def answer_info_query(inline_query):
    username = inline_query.from_user.username
    user_id = inline_query.from_user.id
    name = inline_query.from_user.first_name
    info_article = telebot.types.InlineQueryResultArticle(
        id='0',
        title='Send info',
        description='Send information about me',
        thumb_url=
        'https://png.pngtree.com/element_origin_min_pic/00/00/06/12575cb9a51ad34.jpg',
        thumb_width=512,
        thumb_height=512,
        url=
        'https://png.pngtree.com/element_origin_min_pic/00/00/06/12575cb9a51ad34.jpg',
        input_message_content=
        telebot.types.InputTextMessageContent(
            message_text=
            'My info:\n@{}\nId: {}\nFirst: {}'.format(
                username, user_id, name
            )
        )
    )

    bot.answer_inline_query(
        switch_pm_text='To bot messages',
        switch_pm_parameter='from_pm',
        inline_query_id=inline_query.id,
        results=[info_article],
        cache_time=0
    )