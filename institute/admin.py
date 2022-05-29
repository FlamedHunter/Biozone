from django.contrib import admin

from institute.models import Institute
from django.contrib import admin
# Register your models here.


class InstituteAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('institute_name',)}
    list_display = ('institute_name', 'slug')

admin.site.register(Institute, InstituteAdmin)