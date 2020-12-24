from django.contrib import admin

from .models import Client, KeyPair, Application

admin.site.register(Client)
admin.site.register(KeyPair)
admin.site.register(Application)
