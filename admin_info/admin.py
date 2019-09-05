from django.contrib import admin
from admin_info.models import BrokenPackage

class BPAdmin(admin.ModelAdmin):
    list_display = ('description', 'data' , 'sendTime')
    # fields = ['data', 'description', 'sendTime']

admin.site.register(BrokenPackage, BPAdmin)

# Register your models here.
