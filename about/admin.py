from django.contrib import admin
from .models import (
    AboutUs,
    Contact,
)
# Register your models here.

class AboutUsAdmin(admin.ModelAdmin):
    pass

class ContactAdmin(admin.ModelAdmin):
    pass

admin.site.register(AboutUs,AboutUsAdmin)
admin.site.register(Contact,ContactAdmin)