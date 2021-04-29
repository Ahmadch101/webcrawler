from django.contrib import admin
from .models import Movies,ProjectDetail

# Register your models here.
@admin.register(Movies)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title','hash','pdf_path')

@admin.register(ProjectDetail)
class ProjectDetailAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProjectDetail._meta.get_fields()]
    search_fields = ('title',)