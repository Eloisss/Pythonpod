import vk


# функция получения списка членов группы
def get_members(api, group_id):
    # получение 1000 первых членов группы
    resp = api.groups.getMembers(group_id=group_id)
    count = resp['count']
    members = []
    while count > len(resp):
        resp = api.groups.getMembers(group_id =group_id, offset = len(members))
        members.push(resp)
    return members


#функция получения постов со стены
def get_posts(api, group_id):
    resp = api.wall.get(owner_id=-group_id, count=100, offset=0)
    count = resp['count']
    posts = resp[1:]
    while len(posts) < count:
        resp = api.wall.get(owner_id=-group_id, count=100, offset=len(posts))
        posts.extend(resp[1:])
    return posts

def get_likes(api, group_id):
    members = get_members(api, group_id)
    posts = get_posts(api, group_id)
    members_likes = {}
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
                members_likes.extend(id)
                members_likes[id] += 1 #увеличиваем "счётчик" участника с каждым лайком
            else:
                continue
    return members_likes





def main():
    # открываем сессию
    session = vk.Session(access_token='token')
    # создаем api
    api = vk.API(session)
    likes = get_likes(api, group_id=160694135)
    print(likes)

if __name__ == "__main__":
    main()
