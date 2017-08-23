from time import sleep  
from instagram.client import InstagramAPI
import logging

access_token = 
api = InstagramAPI(access_token=access_token,  
                    client_secret="")

recent_media, next_ = api.user_recent_media(user_id="5921677419", count=10)
# recent_media = InstagramFeed.get_media(user_id="201520509", count=10)

# for media in recent_media:
#    print media.caption.text

# recent_media, url = api.tag_recent_media(tag_name="coding", count=5) # 1

for media in recent_media:  
    # Where the media is
    id_ = media.id
    print id
    # List of users that like the image
    users = [user.username for user in media.likes]
    print users
    # If you have already like the picture, do nothing
    if "YOUR USERNAME" in users:
        print("IN PHOTO")

    # If you haven't liked the photo then do it
    else:
        print("LIKING PICTURE")
        api.like_media(media_id=id_)

    # Sleep to make instagram stop complaining
    sleep(2)

    
