import vk
from rate import rate_limited

session = vk.Session()

group_id = it_mentor
vk_api.VkApi(token ='d828badf019062a767286bfa61a46078ed6ac676ff956190873fe2b36dd07c05716f06447dfe183d42f43') 
vk.auth()
url = "https://api.vk.com/method/execute?"

i = 0;
members = [];
offset = 0;
while(i < 2){
resp = API.groups.getMembers({"group_id": ' +str(group_id)+ ', "offset": var = offset, "fields"
: "can_write_private_message"});
members.push(resp);
i = i + 1;
offset = offset + 1000;
}
return members;
