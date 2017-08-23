#!/usr/bin/env python
'''
Created on Aug 23, 2017

@author: tzungtzu
'''

from instagram.client import InstagramAPI
from ConfigParser import SafeConfigParser
import argparse
import datetime
import logging


# access_token = "201520509.8629611.ad297e6e2c984d52be4c9d14a9385482"  
# client_secret = "4de7846a50ff42cfa087c8383e20d4ad"
# username = "tzungtzu.test,tzungtzu"
# log_path = "log/like-my-gf.log"

config_parser = SafeConfigParser()
config_parser.read('config.ini')

arg_parser = argparse.ArgumentParser(description='Auto-like my GF\'s Instagram')
arg_parser.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity')
args = arg_parser.parse_args()


CONFIG = dict( client_id     = config_parser.get('Client', 'client_id'),
               client_secret = config_parser.get('Client', 'client_secret'),
               redirect_uri  = config_parser.get('Client', 'redirect_uri'),
                 )
OTHER = dict( access_token = config_parser.get('Access Token', 'access_token'),
              target       = config_parser.get('Target', 'username'),
              log_path     = config_parser.get('Path', 'log_path')+'like-my-gf.log',
    )

if args.verbose:
    logging.basicConfig(filename=OTHER['log_path'], level=logging.DEBUG)
else:
    logging.basicConfig(filename=OTHER['log_path'], level=logging.INFO)



def auth_request():  
    api = InstagramAPI(access_token=OTHER['access_token'],client_secret=CONFIG['client_secret'])
    target_ids = api.user_search(OTHER['target'],1)
    if len(target_ids) > 1:
        logging.error('Found mutiple users, please check username')
        return

    target_id = target_ids[0].id
    my_name   = api.user().username
    logging.debug('Starting check recent media')
    recent_media, url = api.user_recent_media(user_id=target_id, count = 1)
    liked_media = []
    for media in recent_media:
        logging.debug('Processing media %s' % media.id)
        users = api.media_likes(media.id)
        will_like = True
        for user in users:
            if user.username == my_name:
                will_like = False
                break
        if will_like:
            logging.debug('Liking media %s' % media.id)
            api.like_media(media.id)
            liked_media.append(media)
        else:
            logging.debug('Already liked media %s, aborting like' % media.id)

    return liked_media

if __name__ == '__main__':
    if OTHER['access_token'] == 'None':           # Not mistake, but default token is 'None' but not None
        print "no access_token"
    liked_media = auth_request()
    if len(liked_media) > 0:
        logging.info('-'*10+str(datetime.datetime.now())+'-'*10)
        logging.info('-'*10+'Liked '+str(len(liked_media))+' medias'+'-'*10)