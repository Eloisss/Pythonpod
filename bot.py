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
def get_posts(api, group_id, dict):
    resp = api.wall.get(owner_id=-group_id, count=100, offset=0)
    count = resp[0]
    posts = resp[1:]
    while len(posts) < count:
        resp = api.wall.get(owner_id=-group_id, count=100, offset=len(posts))
        posts.extend(resp[1:])
    return posts

def get_likes(api, post_id, dict):
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
                dict[like['id']] += 1 #увеличиваем "счётчик" участника с каждым лайком
            else:
                continue

def get_treposts(api, post_id, dict):
    for post in posts:
        # берем количество репостов
        count = post['reposts']['count']
        # если их нет - берем следующий пост
        if count == 0:
            continue
        response = api.wall.getReposts(owner_id=-group_id, post_id=post_id, count=1000, offset=response_count * 1000)
        for repost in response['items']:
            if datatime.today - datatime.fromtimestamp(int(repost["date"])) < datatime.timedelta(14):
                dict[repost["from_id"]] += 1
            else:
                continue


def get_tcomments(api, post_id, dict):
    for post in posts:
        # берем количество репостов
        count = post['count']
        response_count = 0
        # если их нет - берем следующий пост
        if count == 0:
            continue
        resp = api.wall.getComments(owner_id=-group_id, post_id=post_id, count=1000, offset=response_count * 1000)
        for com in resp['items']:
            if datatime.today - datatime.fromtimestamp(int(repost["date"])) < datatime.timedelta(14):
                dict[com["from_id"]] += 1
            else:
                continue

def get_activities(api, group_id):
    members = get_members(api, group_id)
    member_activities = fromkeys(members, 0)
    posts = get_posts(api, group_id)
    for post in posts:
       get_treposts(api, post["id"], member_activities)
       get_tcomments(api, post["id"], member_activities)
       get_likes(post[api], post["id"], member_activities)

   idle_members = sorted(member_activities, key=lambda t:t[0])
   print(idle_members)

def main():
    # открываем сессию
    session = vk.Session(access_token='7a8dd9837a8dd9837a8dd983197aed001977a8d7a8dd98320e716a57d3cad75afbb2372')
    # создаем api
    api = vk.API(session)
    active = get_activities(api, group_id=160694135)
    print(active)

if __name__ == "__main__":
    main()