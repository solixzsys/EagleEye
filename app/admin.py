from django.contrib import admin
from app.models import *

class EntryDisplay(admin.ModelAdmin):
    list_display=("heading","page","thumbnail","date","channel")

class StoryDisplay(admin.ModelAdmin):
    list_display=("heading","content")

admin.site.register(Country)
admin.site.register(Channel)
admin.site.register(Story,StoryDisplay)
admin.site.register(Entry,EntryDisplay)