from datas import token, access_token
import vk_api
from vk_api.utils import get_random_id
import requests
import praw
import urllib.request
import json
from datas import APP_ID, APP_SECRET, group_id
import datetime, calendar
from datetime import date

vk = vk_api.VkApi(token=token)

vk_user = vk_api.VkApi(token=access_token)

actions = {"буп": ["😬", "бупнул"], "бупнуть": ["😬", "бупнул"], "боньк": ["🏏", "бонькнул"],
           "бонькнуть": ["🏏", "бонькнул"]}

reddit = praw.Reddit(
    client_id=APP_ID,
    client_secret=APP_SECRET,
    user_agent="redditdev scraper by vk group PSA union",
)

last_date = datetime.date.today()
counter = 0


def vk_print(message: str, chat_id, reply=None, attachment=None):
    vk.method('messages.send',
              {'chat_id': chat_id,
               'message': message,
               'random_id': get_random_id(),
               "reply_to": reply,
               "disable_mentions": 1,
               "attachment": attachment})


def vk_delete(message_id: int):
    vk.method("messages.delete",
              {"message_ids": message_id,
               "delete_for_all": 1})


def want_function(message: str) -> str:
    emotions = {'огурцы': "🥒🥒🥒", 'огурец': "🥒", "печеньки": '🍪🍪🍪', 'пиво': '🍺🍺🍺', 'квас': '🍺🍺🍺', 'чай': '☕☕☕',
                'вино': '🍸🍸🍸', 'пиццу': '🍕🍕🍕'}
    message = message[5:].split()
    if message[0][-2:] == 'ть':
        message = ' '.join(message)
        return 'иди ' + message + " "
    message = ' '.join(message)
    if message in emotions:
        return 'держи ' + message + " " + emotions[message]
    return 'держи ' + message + " "


def action(message_id: int, text: str) -> str:
    message_data = vk.method("messages.getById",
                             {"message_ids": message_id,
                              "extended": 1})['items'][0]
    person_one = message_data['from_id']
    person_two = message_data['reply_message']['from_id']

    member_data1 = vk.method('users.get',
                             {'user_ids': person_one,
                              'fields': 'domain'})[0]
    domain1 = member_data1['domain']
    first_name1 = member_data1['first_name']
    last_name1 = member_data1['last_name']

    member_data2 = vk.method('users.get',
                             {'user_ids': person_two,
                              'fields': 'domain'})[0]
    domain2 = member_data2['domain']
    first_name2 = member_data2['first_name']
    last_name2 = member_data2['last_name']

    return (f"{actions[text][0]} | [{domain1}|{first_name1} {last_name1}] "
            f"{actions[text][1]} [{domain2}|{first_name2} {last_name2}]")


def group_members() -> int:
    return vk.method('groups.getMembers',
                     {'group_id': f'club{group_id}'})['count']


def check_members(event_type: int, member_id: int) -> str:
    events = {6: "зашёл", 7: "вышел"}
    member_data = vk.method('users.get',
                            {'user_ids': member_id,
                             'fields': 'domain'})[0]
    domain = member_data['domain']
    first_name = member_data['first_name']
    last_name = member_data['last_name']

    return f'[{domain}|{first_name} {last_name}] {events[event_type]}'

def take_vk_info(url) -> dict:
    urls = []
    id_post = url.split("wall")[-1]
    vk.method("wall.getById", {
        "posts": id_post
    })


def take_subreddit_info(url) -> dict:
    urls = []
    url = url[:-1] + ".json"
    responce = urllib.request.urlopen(url)
    with responce as url_data:
        # title - заголовок data[0]["data"]["children"][0]["data"]["title"]
        # author - автор data[0]["data"]["children"][0]["data"]["author"]
        data = json.load(url_data)[0]["data"]["children"][0]["data"]
        url = data["url_overridden_by_dest"]
        if "gallery" in url:
            submission = reddit.submission(url=url)
            image_dict = submission.media_metadata
            for image_item in image_dict.values():
                largest_image = image_item['s']
                image_url = largest_image['u']
                urls.append(image_url)

            reddit_data = {"url": urls,
                           "title": data["title"],
                           "author": data["author"]}
        else:
            reddit_data = {"url": [url],
                           "title": data["title"],
                           "author": data["author"]}
        return reddit_data


def pic_in_album(album_id: int, format_pic: str):
    upload_url = vk_user.method("photos.getUploadServer", {
        "album_id": album_id,
        "group_id": group_id
    })["upload_url"]

    res = requests.post(upload_url, files={'photo': open(f'Pictures/image.{format_pic}', 'rb')}).json()
    print(res)
    photo = vk_user.method("photos.save", {
        "album_id": album_id,
        "group_id": group_id,
        "server": res["server"],
        "photos_list": res["photos_list"],
        "hash": res["hash"]
    })[0]
    return photo


def load_pic_album(pic_urls: list, tags: str) -> str:
    album_links = []
    extend = ["png", "jpg", "jpeg"]
    for pic_url in pic_urls:
        format_pic = pic_url[-3:]  # получаем формат изображения png или jpg
        if format_pic == "peg":
            format_pic = "jpeg"
        if format_pic not in extend:
            format_pic = "png"
        out = open(f"Pictures/image.{format_pic}", "wb")  # сохраняем фото на компьютер
        out.write(requests.get(pic_url).content)
        out.close()
        if "к" in tags:
            if "п" in tags:
                photo = pic_in_album(album_id=302400109, format_pic=format_pic)
            if "с" in tags:
                photo = pic_in_album(album_id=302400112, format_pic=format_pic)
            if "а" in tags:
                photo = pic_in_album(album_id=302400146, format_pic=format_pic)
        else:
            if "п" in tags:
                photo = pic_in_album(album_id=302400080, format_pic=format_pic)
            if "с" in tags:
                photo = pic_in_album(album_id=302400083, format_pic=format_pic)
            if "а" in tags:
                photo = pic_in_album(album_id=302400102, format_pic=format_pic)

        photo_link = f"photo{photo["owner_id"]}_{photo['id']}"
        album_links.append(photo_link)

    return ",".join(album_links)


def post(message: str, attachments: str, url_copyright: str):
    global last_date, counter
    li = [[14, 00, 00], [17, 00, 00], [20, 00, 00], [23, 00, 00]]
    year, month, day = map(int, str(last_date).split("-"))
    if date(year, month, day).weekday() == 4:
        counter += 1
    i = 0
    while True:
        time_tuple = (year, month, day, li[i][0], li[i][1], li[i][2])
        timestamp = calendar.timegm(time_tuple) - 7 * 3600 + counter * 86400
        data = {
            'access_token': access_token,
            "owner_id": -group_id,
            'from_group': 1,
            'message': message,
            "publish_date": timestamp,
            "attachments": attachments,
            "copyright": url_copyright,
            'v': "5.92"}
        years, months, days = map(int,
                                  str(datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')).split("-"))
        i += 1
        if date(years, months, days).weekday() != 4:
            r = requests.post('https://api.vk.com/method/wall.post', data).json()
            if "response" in r:
                counter = 0
                last_date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')
                break
        if i == 4:
            i = 0
            counter += 1
