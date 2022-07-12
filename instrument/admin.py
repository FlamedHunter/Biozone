from django.contrib import admin

from instrument.models import Instrument
# from instrument.models import Instrument_Manager
from django.contrib import admin
# Register your models here.

class InstrumentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('instrument_name',)}
    list_display = ('instrument_name', 'slug', 'category', 'institute',)  

    # def save_model(self, request, obj, form, change):
    #     obj.added_by = request.user
    #     super().save_model(request, obj, form, change)  

admin.site.register(Instrument, InstrumentAdmin)
# admin.site.register(Instrument_Manager)