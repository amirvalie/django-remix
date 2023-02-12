from django.contrib import admin
from .models import (
    About,
    Contact,
)
# Register your models here.

class AboutAdmin(admin.ModelAdmin):
    pass

class ContactAdmin(admin.ModelAdmin):
    pass

admin.site.register(About,AboutAdmin)
admin.site.register(Contact,ContactAdmin)