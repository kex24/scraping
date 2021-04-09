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


# Config
url_base = 'https://www.bdsmlife.cz/inzeraty.htm?pg='
tags = ['submisivního muže', 'switch muže', 'submisivní ženu nebo muže',
        'switch ženu nebo muže']
pages = 2
date_format = '%d.%m.%Y %H:%M'
check_file_path = 'dslife_scraper_last_check.txt'


# Reading last check date
if os.path.isfile(check_file_path):
    date_file = open(check_file_path, 'r')
    last_check = date_file.read()
    date_file.close()
    last_check = datetime.strptime(last_check, date_format)
else:
    last_check = datetime(2000, 1, 1)


# Main loop
ads_found = []
for p in range(1,pages+1):
    # Load page
    url = url_base + str(p)
    webClient = urlopen(url)
    page = webClient.read()
    webClient.close()
    
    # Parse page
    page = soup(page, 'html.parser')
    
    # Find ads
    ads = page.findAll('div',{'class': 'inzerat'})
    
    # Check ads
    for ad in ads:
        ad_date = str(ad.findAll('div',{'class': 'datum new'})[0]).split(' - ')[1].split('<')[0]
        ad_date = datetime.strptime(ad_date, date_format)
        if ad_date > last_check:
            ad_header = str(ad.findAll('div',{'class': 'typ'})[0])
            for tag in tags:
                if tag in ad_header:
                    ad_text = str(ad.findAll('div',{'class': 'txt'})[0])
                    
                    to_omit = ['<div class="typ">', '<span class="kraj">',
                               '</span>', '</div>', '<div class="txt">']
                    for subs in to_omit:
                        ad_header = re.sub(r'{0}'.format(subs), '', ad_header)
                        ad_text = re.sub(r'{0}'.format(subs), '', ad_text)
                    
                    
                    ad = f'{ad_header}\n{ad_text}'
                    ads_found.append(ad)
                    print()
                    print(ad)


# If nothing new
if len(ads_found) == 0:
    print('No new ads')
else:
    address = 'mrt.sevcik@gmail.com'
    subject = 'DSlife notification'
    body = '{0} new ads found for you!'.format(len(ads_found))
    
    send_mail(address, subject, body)


# Writing last check date
date_file = open(check_file_path, 'w')
date_file.write(datetime.now().strftime(date_format))
date_file.close()

