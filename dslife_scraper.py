# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 20:51:38 2021

@author: kex
"""

import os
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from datetime import datetime
from mailing import send_mail
import re
import json
import io


print('[{0}] Starting script: {1}'.format(
    datetime.now().strftime('%d.%m.%Y %H:%M'),os.path.basename(__file__)))

# Config
with io.open('config.json', 'r', encoding='UTF-8') as f:
    CONFIG=json.loads(f.read())


# Reading last check date
if os.path.isfile(CONFIG['check_file_path']):
    date_file = open(CONFIG['check_file_path'], 'r')
    last_ad_id = date_file.read()
    date_file.close()
    last_ad_id = int(last_ad_id)
else:
    last_ad_id = 0
if CONFIG['debug']:
    print(f'Last ad ID was: {last_ad_id}')

# Main loop
ads_found = []
ad_ids = []
for p in range(1,CONFIG['pages']+1):
    # Load page
    url = CONFIG['url_base'] + str(p)
    webClient = urlopen(url)
    page = webClient.read()
    webClient.close()
    
    # Parse page
    page = soup(page, 'html.parser')
    
    # Find ads
    ads = page.findAll('div',{'class': 'inzerat'})
    
    # Check ads
    for ad in ads:
        # Print ad for debuging
        if CONFIG['debug']:
            print()
            print(ad)
            print()
        
        # Parse as ID
        ad_id = int(str(ad.findAll('div',{'class': 'number'})[0]).split(
            '#')[1].split('<')[0])
        ad_ids.append(ad_id)
        
        # Check if the ad is new
        if ad_id > last_ad_id:
            
            # Parse header
            ad_header = str(ad.findAll('div',{'class': 'typ'})[0])
            for tag in CONFIG['tags']:
                
                # Check tag
                if tag in ad_header:
                    
                    ad_text = str(ad.findAll('div',{'class': 'txt'})[0])
                    
                    to_omit = ['<div class="typ">', '<span class="kraj">',
                               '</span>', '</div>', '<div class="txt">']
                    for subs in to_omit:
                        ad_header = re.sub(r'{0}'.format(subs), '', ad_header)
                        ad_text = re.sub(r'{0}'.format(subs), '', ad_text)
                    
                    
                    ad = f'{ad_header}\n{ad_text}'
                    ads_found.append(ad)
                    if CONFIG['debug']:
                        print(f'Ad {ad_id} appended')


# If nothing new
if len(ads_found) == 0:
    print('No new ads')
else:
    address = 'mrt.sevcik@gmail.com'
    subject = 'DSlife notification'
    body = '{0} new ads found for you!'.format(len(ads_found))
    
    print(body)
    print('Sending mail ...')
    send_mail(address, subject, body)


# Writing last check date
date_file = open(CONFIG['check_file_path'], 'w')
date_file.write(str(max(ad_ids)))
date_file.close()

print('FINISHED')

