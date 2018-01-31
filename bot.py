import vk


# функция получения списка членов группы
def get_members(api, group_id):
    # получение 1000 первых членов группы
    resp = api.groups.getMembers(group_id=group_id)
    count = resp['count']
    members = []
    while count > len(members):
        resp = api.groups.getMembers(group_id =group_id, offset = len(members))
        members.extend(resp['users'])
    return members


#функция получения постов со стены
def get_posts(api, group_id):
    resp = api.wall.get(owner_id=-group_id, count=100, offset=0)
    count = resp[0]
    posts = resp[1:]
    while len(posts) < count:
        resp = api.wall.get(owner_id=-group_id, count=100, offset=len(posts))
        posts.extend(resp[1:])
    return posts

def get_likes(api, group_id):
    members = get_members(api, group_id)
    posts = get_posts(api, group_id)
    members_likes = dict.fromkeys(members, 0)
    for post in posts:
        #для каждого поста получаем список лайков
        resplikes = api.likes.getList(type='post', owner_id=-group_id, item_id=post['id'])
        #для каждого поста создаём список с лайками
        getlikes = resplikes['users']
        #узнаём кол-во лайков
        count = resplikes['count']
        if count == 0:
            continue
        #проверяем всех, кто лайкнул:
        for id in getlikes:
            #проверяем каждого, кто лайкнул, есть ли он в участниках группы
            if id in members: # and ('тут условие, что участник лайкнул более 1 раза за 14 дней'):
                members_likes[id] += 1 #увеличиваем "счётчик" участника с каждым лайком
            else:
                continue
    return members_likes

def get_timereposts(api, group_id):
    members = get_members(api, group_id)
    # создаем словарь, где ключ - id пользователя, значения - 0
    users = dict.fromkeys(members, 0)
    posts = get_posts(api, group_id)
    for post in posts:
        # берем количество репостов
        count = post['reposts']['count']
        # если их нет - берем следующий пост
        if count == 0:
            continue
        response = api.wall.getReposts(owner_id=-group_id, post_id=post_id, count=1000, offset=response_count * 1000)
        for repost in response['items']:
            if datatime.today - datatime.fromtimestamp(int(repost["date"])) < datatime.timedelta(14):
                users[repost["from_id"]] += 1
    return users


def main():
    # открываем сессию
    session = vk.Session(access_token='7a8dd9837a8dd9837a8dd983197aed001977a8d7a8dd98320e716a57d3cad75afbb2372')
    # создаем api
    api = vk.API(session)
   # likes = get_likes(api, group_id=160694135)
    likes = get_likes(api, group_id=160694135)
    print(likes)

if __name__ == "__main__":
    main()
