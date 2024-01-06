from vk_api.longpoll import VkLongPoll, VkEventType
from modules import vk, action, actions, post
from modules import (load_pic_album, take_subreddit_info, group_members, vk_print, vk_delete, want_function,
                     check_members)
from datas import white_list

longpoll = VkLongPoll(vk)

# print(vk.method("wall.post", {""}))
if __name__ == "__main__":
    print("Запущен")
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.CHAT_UPDATE:
                    vk_print(message=check_members(member_id=event.info['user_id']),
                             event_type=event.type_id,
                             chat_id=event.chat_id)

                if event.type == VkEventType.MESSAGE_NEW:
                    msg = event.text.lower()
                    if msg[:5] == '/пост' and event.user_id in white_list: #реддит
                        counter = 0
                        vk_print(message="постимс", chat_id=event.chat_id)
                        datas = msg[5:].split("\n")[1:]
                        print(datas)
                        for data in datas:
                            counter += 1
                            print(data)
                            link, tags = map(str, data.split())
                            print(link)
                            print(tags)
                            reddit_data = take_subreddit_info(link)

                            url = reddit_data["url"]
                            title = reddit_data["title"]
                            author = reddit_data["author"]

                            album_links = load_pic_album(url, tags)
                            print(album_links)
                            message = f"{title}\n\nАвтор: {author}\n\n #Furry #Фурри"
                            if "п" in tags:
                                message = message + " #Protogen #Протоген"
                            if "c" in tags:
                                message = message + " #Synth #Синт"
                            if "a" in tags:
                                message = message + " #Ampwave #Ампвейв"
                            if "к" in tags:
                                message = message + " #Сьют #Fursuit #Фурсьют"
                            if "р" in tags:
                                message = message + " #Ру_автор #RU"
                            post(message=message,
                                 attachments=album_links,
                                 url_copyright=link)
                            vk_print(message=f"Выложен {counter} пост!",
                                     chat_id=event.chat_id,
                                     reply=event.message_id)


                    if msg == "количество":
                        vk_print(message=f"Количество участников в группе: {group_members()}!",
                                 chat_id=event.chat_id,
                                 reply=event.message_id)

                    if msg[:4] == "хочу":
                        vk_print(message=want_function(message=msg),
                                 chat_id=event.chat_id,
                                 reply=event.message_id)

                    if msg == "пёс" or msg == "пес":
                        vk_print(message="Бот умеет следующее:\n"
                                         "Количество - выводит количество участников в группе PSA Union\n"
                                         "Хочу {фраза} - выводит держи {фраза} или же иди {фраза}\n"
                                         "Буп/Боньк - выполняет действия над пользователем которому отвечаешь",
                                 chat_id=event.chat_id,
                                 reply=event.message_id)

                    if msg in actions:
                        vk_print(message=action(message_id=event.message_id, text=msg),
                                 chat_id=event.chat_id)

        except Exception as ex:
            print(ex)
