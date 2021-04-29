#!/usr/bin/env python

import os
cwd = os.getcwd()
print(cwd)
os.chdir(cwd)


from subprocess import call
def crawl():
    crawler_names = [
        'backstage-crawl',
        'britishcouncil-crawl',
        'dallasfilm-crawl',
        'filmcatalogue',
        'filmcommission-crawl',
        'filmneworleans',
        'fortissimofilms-crawl',
        'fortitudeint',
        'futoncritic',
        'imagineentertainment-crawl',
        'imdb-crawl',
        'kasbah',
        'louisianaentertainment',
        'mediafusionent-crawl',
        'movieinsider-crawl',
        'premierepicture-crawl',
        'projectcasting-crawl',
        'screenaustralia-crawl',
        'texasfilmcommission-crawl',
        'webtenerife-crawl',
        '13films-crawl',
        'altitudefilment-crawl',
        'filmvic',
        'findfilmwork-crawl',
        'njgov',
        'screensiren-crawl',
        'SeeSawFilms-crawl',
        'whatsfilming'
    ]

    for c_name in crawler_names:
        call('scrapy crawl {}'.format(c_name), shell=True)
