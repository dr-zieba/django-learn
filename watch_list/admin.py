from django.contrib import admin
from .models import WatchList, Platform, Review

# Register your models here.
admin.site.register(WatchList)
admin.site.register(Platform)
admin.site.register(Review)
