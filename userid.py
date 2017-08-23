from time import sleep  
from instagram.client import InstagramAPI
import logging

access_token = ""
api = InstagramAPI(access_token="",  
                    client_secret="")
username = "ran_yu_"

target_ids = api.user_search(username,1)
print target_ids
target_id = target_ids[0].id
print target_id
