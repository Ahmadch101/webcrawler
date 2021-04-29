import datetime
import hashlib
import re

import pdfkit
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
from django.forms.models import model_to_dict
import os
import json
from uuid import uuid4
cwd = os.getcwd()
print(cwd)
from .models import Movies,ProjectDetail
os.chdir(cwd)
from ScrappingApplication.run_script import crawl
# Create your views here.
FILE_PATH = cwd+"/letter"
from crawlerapp.html_format import html_format_t,header,footer
def Home(request):
    # Movies.objects.all().delete()
    # ProjectDetail.objects.all().delete()
    return render(request,"index.html")

def join_fields(value, joiner):
    if isinstance(value, list):
        return f'{joiner} '.join(value)
    return value

def fix_movie_info(movie):
    new_movie = movie.copy()

    if not movie.get('project_issue_date'):
        new_movie['project_issue_date'] = movie.get('release_date', 'N\A')

    if not new_movie.get('project_start_date'):
        new_movie['project_start_date'] = movie.get('project_issue_date', 'N\A')

    current_date = datetime.datetime.now().strftime('%d %B %Y')
    new_movie['project_issue_date1'] = movie.get('project_issue_date', 'N\A')
    new_movie['batch_no'] = hashlib.sha224(str(current_date).encode('utf-8')).hexdigest()[:8]
    new_movie['letter_creation_date'] = current_date

    return new_movie

def finduplicate(request):
    allproject=ProjectDetail.objects.all()
    fields_to_end_with_br = [
        'genres', 'locations', 'producers',
        'writers', 'directors', 'cast'
    ]
    fields_to_join = [
        (',', 'plot'),
        (' -', 'cast'),
        (',', 'genres'),
        (' -', 'studios'),
        (' -', 'writers'),
        (' -', 'directors'),
        (' -', 'producers'),
        (' -', 'locations'),
        (',', 'production_companies'),

    ]
    html=""
    head=""
    i=0
    for item in allproject:
        item=model_to_dict(item, fields=[field.name for field in item._meta.get_fields()])
        movie = item.copy()

        for joiner, field in fields_to_join:
            movie[field] = join_fields(movie[field], "-")

        for field in fields_to_end_with_br:
            if movie[field]:
                movie[field] = f'{movie[field]}<br>'

        name_hash = hashlib.sha224(str(item['title']).encode('utf-8')).hexdigest()[:8]
        file_name = f'{name_hash}.pdf'
        file_path = f'{FILE_PATH}/{file_name}'

        movie['listing'] = name_hash

        movie = fix_movie_info(movie)
        if i==0:
            head=header.format(**movie)
        i+=1
        c = html_format_t.format(**movie)
        html=html+c
    html=head+html+footer
    pdfkit.from_string(html, file_path)
    # dupes = ProjectDetail.objects.values('title').annotate(Count('id')).order_by().filter(id__count__gt=1)
    # print(dupes)
    # # m=Movies.objects.filter(title__in=[item['title'] for item in dupes])
    # # print(m)
    # jsonDec = json.decoder.JSONDecoder()
    # a=ProjectDetail.objects.get(title='The Banishing')
    # print(type(a.production_companies))
    # data=a.production_companies.strip('][').split(', ')
    # contactemail=[]
    # contactemailphone = []
    # fax=[]
    #
    # i=0
    # for text in data:
    #     text=text.replace(": ","")
    #     try:
    #
    #         if 'Email' in text:
    #             contactemail.append(data[i+2])
    #         if 'Phone' in text:
    #             contactemailphone.append(data[i+1])
    #         if 'Fax' in text:
    #             fax.append(data[i+1])
    #     except:
    #         print("no")
    #     i+=1
    # print(contactemail)
    # print(contactemailphone)
    # print(fax)
    # data=list(set(data)-set(contactemail))
    # data = list(set(data) - set(contactemailphone))
    # data = list(set(data) - set(fax))
    # print(data)
    # for text in data:
    #     text=text.replace(":","").strip()
    #     text=text.strip()
    #     print(text)
    #     for groups in phoneRegex.findall(text):
    #         print("okk")
    #         print(groups)




    # emptyfield1=[]
    # emptyfield2=[]
    # for feild in ProjectDetail._meta.get_fields():
    #     if getattr(obj1,feild.name)==None or getattr(obj1,feild.name)==[] or getattr(obj1,feild.name)=='[""]' or getattr(obj1,feild.name)=="":
    #         print(feild.name)
    #
    # obj1.save()
    return HttpResponse(request,200)

def runcrawler(request):
    crawl()
    # unique_id = str(uuid4())
    #
    # settings = {
    #     'unique_id': unique_id,  # unique ID for each record for DB
    #     'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    # }
    # task = scrapyd.schedule('default', 'imdb-crawl',
    #                        settings=settings)
    #
    # return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started'})
    # crawler_names = [
    #     'backstage-crawl',
    #     'britishcouncil-crawl',
    #     'dallasfilm-crawl',
    #     'filmcatalogue',
    #     'filmcommission-crawl',
    #     'filmneworleans',
    #     'fortissimofilms-crawl',
    #     'fortitudeint',
    #     'futoncritic',
    #     'imagineentertainment-crawl',
    #     'imdb-crawl',
    #     'kasbah',
    #     'louisianaentertainment',
    #     'mediafusionent-crawl',
    #     'movieinsider-crawl',
    #     'premierepicture-crawl',
    #     'projectcasting-crawl',
    #     'screenaustralia-crawl',
    #     'texasfilmcommission-crawl',
    #     'webtenerife-crawl',
    #     '13films-crawl',
    #     'altitudefilment-crawl',
    #     'filmvic',
    #     'findfilmwork-crawl',
    #     'njgov',
    #     'screensiren-crawl',
    #     'SeeSawFilms-crawl',
    #     'whatsfilming'
    # ]
    # for c_name in crawler_names:
    #     call('scrapy crawl {}'.format(c_name), shell=True)
    return redirect('Home')