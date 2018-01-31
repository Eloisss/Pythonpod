import vk
from rate import rate_limited


# функция получения списка членов группы
def get_members(api, group_id):
    # получение 1000 первых членов группы
    resp = api.groups.getMembers(group_id=group_id)
    count = resp['count']
    members = [];
    while count > len(resp):
        resp = API.groups.getMembers(group_id = group_id, offset = len(members))
        members.push(resp)
    return members


#функция получения постов со стены
def get_posts(api, group_id):
    resp = api.wall.get(group_id=group_id, count=100, offset=0)
    count = resp['count']
    posts = resp[1:]
    while len(posts) < count:
        resp = api.wall.get(group_id=group_id, count=100, offset=len(posts))
        posts.extend(resp[1:])
    return posts

def get_likes(api,):
    members = get_members(api, group_id)
    posts = get_posts(api, group_id)
    members_likes = set()
    for post in posts:
        #для каждого поста получаем список лайков
        resplikes = likes.getList(type=post, group_id=group_id)
        #для каждого поста создаём список с лайками
        getlikes = resp['likes']
        #узнаём кол-во лайков
        count = len(getlikes)
        if count == 0:
            continue
        #проверяем всех, кто лайкнул:
        for id in getlikes:
            #проверяем каждого, кто лайкнул, есть ли он в участниках группы
            if id in members: # and ('тут условие, что участник лайкнул более 1 раза за 14 дней'):
                id += 1
                members_likes.extend(id)
            else:
                continue
    return members_likes






def main():
    session = vk.Session()
    group_id = 158717480
    api.VkApi(token ='7a8dd9837a8dd9837a8dd983197aed001977a8d7a8dd98320e716a57d3cad75afbb2372')
    vk.auth()
    posts = get_posts(api, group_id=group_id)
    print (posts)
    url = "https://api.vk.com/method/execute?"


