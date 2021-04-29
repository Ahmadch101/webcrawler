from django.db import models
import os
cwd = os.getcwd()
print(cwd)
os.chdir(cwd)


from subprocess import call
# Create your models here.

class Movies(models.Model):
    title=models.CharField(max_length=200,verbose_name='Title')
    hash=models.CharField(max_length=200,verbose_name='Hash',null=True,blank=True)
    pdf_path=models.CharField(max_length=200,verbose_name='Pdf Path',null=True,blank=True)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

class ProjectDetail(models.Model):
    url = models.CharField(max_length=200,verbose_name='Url',null=True,blank=True)
    project_id = models.CharField(max_length=200,verbose_name='Project id',null=True,blank=True)
    title = models.CharField(max_length=200,verbose_name='Title',null=True,blank=True)
    aka_title = models.CharField(max_length=200,verbose_name='Aka Title',null=True,blank=True)
    project_type = models.CharField(max_length=200,null=True,blank=True)
    project_issue_date = models.CharField(max_length=200,null=True,blank=True)
    project_issue_date1 = models.CharField(max_length=200,null=True,blank=True)
    project_start_date = models.CharField(max_length=200,null=True,blank=True)
    project_update = models.CharField(max_length=200,null=True,blank=True)
    locations = models.CharField(max_length=200,null=True,blank=True)
    photography_start_date = models.CharField(max_length=200,null=True,blank=True)
    writers = models.CharField(max_length=200,null=True,blank=True)
    directors = models.CharField(max_length=200,null=True,blank=True)
    cast = models.CharField(max_length=200,null=True,blank=True)
    producers = models.CharField(max_length=200,null=True,blank=True)
    production_companies = models.CharField(max_length=200,null=True,blank=True)
    studios = models.CharField(max_length=200,null=True,blank=True)
    plot = models.CharField(max_length=200,null=True,blank=True)
    genres = models.CharField(max_length=200,null=True,blank=True)
    project_notes = models.CharField(max_length=200,null=True,blank=True)
    release_date = models.CharField(max_length=200,null=True,blank=True)
    start_wrap_schedule = models.CharField(max_length=200,null=True,blank=True)
    issue_num = models.CharField(max_length=200,null=True,blank=True)
    listing = models.CharField(max_length=200,null=True,blank=True)
    batch_no = models.CharField(max_length=200,null=True,blank=True)
    letter_creation_date = models.CharField(max_length=200,null=True,blank=True)
    def __str__(self):
        return str(self.id)+"    ---    "+self.title