import boto3
import datetime
import hashlib
import pdfkit
import sqlite3
import json
import time
import logging
import requests
from crawlerapp.models import Movies,ProjectDetail


path=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path)
from botocore.client import Config

from .settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, FILE_PATH, DB_PATH

from .html_format import html_format_t

logger = logging.getLogger()


class ScrappingapplicationPipeline:
    must_haves = [
        # 'title', 'production_companies', 'locations'
    ]
    def process_item(self, item, spider):
        for field in self.must_haves:
            if not item.get(field):
                logger.warning(f'Droping item because {field} is not available!')
                return {}
        
        return item


# This pipeline takes the Item and convert it into PDF and save content in DB
class  ScrappingSqLitePipeline(object):
    # Take the item and put it in database - do not allow duplicates
    def process_item(self, item, spider):
        moviev=Movies()
        project=ProjectDetail()
        moviev.title=item['title']
        id=moviev.save()
        print("iddd")
        print(id)
        item=self.fix_movie_info(item)
        if 'issue_num' in item:
            if item['issue_num']=="":
                item['issue_num']=id
        result=ProjectDetail.objects.filter(title=item['title'])
        if len(result)>0:
            for feild in ProjectDetail._meta.get_fields():
                if getattr(result[0], feild.name) == None or getattr(result[0], feild.name) == [] or getattr(result[0],feild.name) == '[""]' or getattr(result[0], feild.name) == "" or getattr(result[0], feild.name) == "N/A":
                    print(feild.name)
                    if item[feild.name]!=None or item[feild.name]!=[""] or item[feild.name]!=[] or item[feild.name]!='[""]' or item[feild.name]!="":
                        if feild.name == 'project_id':
                            if 'id' in item:
                                setattr(result[0], 'project_id', item['id'])
                            else:
                                setattr(result[0], 'project_id', id)
                        else:
                            setattr(result[0],feild.name,item[feild.name])
            result[0].save()
        else:
            with open('ScrappingApplication/findfilmwork.json') as f:
                data = json.load(f)
            output_dict = [x for x in data if x['title'] == item['title']]
            if len(output_dict)>0:
                filmdata=output_dict[0]
                print(filmdata)
            project=ProjectDetail()
            for field in ProjectDetail._meta.get_fields():
                if  len(output_dict)>0:
                    print("function call")
                    if field.name == 'project_id':
                        setattr(project, 'project_id', filmdata['id'])
                    else:
                        if field.name in filmdata:
                            setattr(project, field.name, filmdata[field.name])
                else:
                    if field.name in item:
                        if field.name=='project_id':
                            if 'id' in item:
                                setattr(project, 'project_id', item['id'])
                            else:
                                setattr(project, 'project_id', id)
                        else:
                            if isinstance(item[field.name],list):
                                setattr(project,field.name,json.dumps(item[field.name]))
                            else:
                                setattr(project,field.name,item[field.name])
            project.save()
        # item['issue_num'] = id
        # project.url=item['url']
        # project.project_id=item['id']
        # project.title=item['title']
        # project.aka_title=item['aka_title']
        # project.project_type=item['project_type']
        # project.project_issue_date=item['project_issue_date']
        # project.project_issue_date1=item['project_issue_date1']
        # project.project_start_date=item['project_start_date']
        # if 'project_update' in item:
        #     project.project_update=item['project_update']
        # project.locations=json.dumps(item['locations'])
        # project.photography_start_date=item['photography_start_date']
        # project.writers=json.dumps(item['writers'])
        # project.directors=json.dumps(item['directors'])
        # project.cast=json.dumps(item['cast'])
        # project.producers=json.dumps(item['producers'])
        # project.production_companies=json.dumps(item['production_companies'])
        # project.studios=json.dumps(item['studios'])
        # project.plot=item['plot'][0]
        # project.genres=json.dumps(item['genres'])
        # if 'project_notes' in item:
        #     project.project_notes=str(item['project_notes'])
        # project.release_date=item['release_date']
        # project.start_wrap_schedule=item['start_wrap_schedule']
        # project.issue_num=item['issue_num']
        # project.save()
        # logger.info("Item saved in db!")
        # print("items")
        time.sleep(3)
        print(item)
        return item

    def fix_movie_info(self, movie):
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



class ScrappingPDFGeneratorPipeline:
    fields_to_end_with_br = [
        'genres','locations', 'producers',
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

    def join_fields(self, value, joiner):
        if isinstance(value, list):
            return f'{joiner} '.join(value)
        return value
    
    def fix_movie_info(self, movie):
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

    def upload_file(self, file_path, file_name):
        end_point_url = 'https://s3.eu-west-2.amazonaws.com'
        credentials = {
            'aws_access_key_id': AWS_ACCESS_KEY_ID, 
            'aws_secret_access_key': AWS_SECRET_ACCESS_KEY
        }
        s3_client = boto3.client('s3', region_name='eu-west-2', endpoint_url=end_point_url, config=Config(signature_version='s3v4'), **credentials)
        
        try:
            with open(file_path, "rb") as f:
                s3_client.upload_fileobj(f, "wppdfupload", file_name)

                # response = requests.post(url=resp, files={file_name: open(file_path, 'rb')})
                logger.info("Uploading file Successfully on S3 bucket")
                
                file_url_on_s3 = f'https://wppdfupload.s3.amazonaws.com/{file_name}'
                logger.info("URL is Generated!")

                req_url = "https://productiontelegram.com/wp-json/api-k/v1/pdf-links/"
                headers = {}
                headers['Content-Type'] = "application/json"
                # headers['Authorization'] = "Basic dGhlbWFjaGluZTpDdW1ZVmFCYnJQNHQ2S21tRWtZNUdOd3Y="
                headers['cache-control'] = "no-cache"
                # headers['Postman-Token'] = "ab5a85de-2184-4b07-9d72-8016f6786735"
                
                
                payload = {}
                payload['file_name'] = file_name
                payload['file_link'] = file_url_on_s3
                payload['description'] = 'N/A'
                # payload = f"{{\n\t\"file_name\": \"{file_name}\",\n\t\"file_link\": \"{signed_url}\",\n\t\"description\": \"Testing file\"\n}}"
                
                r = requests.post(url=req_url, data=json.dumps(payload), headers=headers)
            
                if r.status_code == 200:
                    logger.info("Uploading file Successfully on Website!")
                    return True
                logger.warning("Uploading file Unsuccessfully")
        except Exception as e:
            return False

    def process_item(self, item, spider):
        if not item:
            return {}
        
        movie = item.copy()

        for joiner, field in self.fields_to_join:
            movie[field] = self.join_fields(movie[field], joiner)

        for field in self.fields_to_end_with_br:
            if movie[field]:
                movie[field] = f'{movie[field]}<br>'

        
        name_hash = hashlib.sha224(str(item['title']).encode('utf-8')).hexdigest()[:8]
        file_name = f'{name_hash}.pdf'
        file_path = f'{FILE_PATH}/{file_name}'
        
        movie['listing'] = name_hash

        movie = self.fix_movie_info(movie)
        
        html = html_format_t.format(**movie)
        pdfkit.from_string(html, file_path,configuration=config)

        if self.upload_file(file_path, file_name):
            logger.info("Uploading file Successfully")
        else:
            logger.warning("Uploading file Unsuccessfully")

        return item
