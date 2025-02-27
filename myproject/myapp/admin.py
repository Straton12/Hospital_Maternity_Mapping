from django.shortcuts import render
from django.contrib import admin
from django.http import HttpResponse
from django.contrib.auth.admin import UserAdmin
from .models import KenyaSubcounty, KenyaCounty, KenyaCountry, Hospitals, level4_buffer, level5_buffer

admin.site.register(KenyaCountry)
admin.site.register(KenyaCounty)
admin.site.register(KenyaSubcounty)
admin.site.register(Hospitals)
admin.site.register(level4_buffer)
admin.site.register(level5_buffer)